from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from twitter.models import Tweet, Followship, Like, Notification, Stream
from twitter.forms import TweetForm, RegistrationForm
from services import share, notify, stream, post, profile_nav

from services import page


def index(request):
    render_data = page.index(request)
    return render(request, 'twitter/index.html', render_data)

def notification(request):
    user = request.user
    notifications = Notification.objects.filter(notified_user=user)
    show_pagination = False
    for n in notifications:
        n.subtitle = notify.get_subtitle(n.notified_type)
        tweet = n.tweet
        if tweet:
            post.get_action_data(tweet, user)

    paginate_by = 10
    notification_list, show_pagination = share.pagination(request, notifications, paginate_by)

    return render(request, 'twitter/notification.html', {
        'notification_list': notification_list,
        'object_list': notification_list,
        'show_pagination': show_pagination,
    })

def profile(request, username):
    login_user = request.user
    visited_user = User.objects.get(username=username)
    
    profile_nav.subnav_sessions(request, login_user, visited_user)
    tweet_list = list(Tweet.objects.filter(author=visited_user))
    tweets = post.show_tweets(tweet_list, visited_user, request.user)
    paginate_by = 10
    tweets, show_pagination = share.pagination(request, tweets, paginate_by)
    return render(request, 'twitter/profile.html', {
        'visited_user': visited_user,
        'tweets': tweets,
        'object_list': tweets,
        'show_pagination': show_pagination,
    })

def following(request, username):
    visited_user = User.objects.get(username=username)
    following_list = Followship.objects.filter(initiative_user=visited_user)
    paginate_by = 10
    followings, show_pagination = share.pagination(request, following_list, paginate_by)
    return render(request, 'twitter/following.html', {
        'visited_user': visited_user,
        'followings': followings,
        'object_list': followings,
        'show_pagination': show_pagination,
    })

def follower(request, username):
    visited_user = User.objects.get(username=username)
    follower_list = Followship.objects.filter(followed_user=visited_user)
    paginate_by = 10
    followers, show_pagination = share.pagination(request, follower_list, paginate_by)
    return render(request, 'twitter/follower.html', {
        'visited_user': visited_user,
        'followers': followers,
        'object_list': followers,
        'show_pagination': show_pagination,
    })

@login_required
def likes(request, username):
    visited_user = User.objects.get(username=username)
    likes = Like.objects.filter(author=visited_user) or []
    like_tweets = post.show_like_tweets(likes, request.user)
    paginate_by = 10
    like_list, show_pagination = share.pagination(request, like_tweets, paginate_by)

    return render(request, 'twitter/likes.html', {
        'visited_user': visited_user,
        'tweets': like_list,
        'object_list': like_list,
        'show_pagination': show_pagination,
    })

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            user = User.objects.create_user(
                request.POST.get('username'),
                request.POST.get('email'),
                request.POST.get('password'),
            )
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {
        'form': form,
    })





@login_required
def post_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            new_tweet = post.create_tweet(request.user, tweet.content, None)
            notify.notify(request.user, new_tweet, Notification.MENTION)
            stream.create_streams(new_tweet, Stream.TWEET)
            return redirect('profile', username=request.user.username)
    else:
        form = TweetForm()
    return render(request, 'twitter/post_tweet.html', {
        'form': form,
    })







@login_required
def follow(request, username):
    login_user = request.user
    visited_user = User.objects.get(username=username)

    if login_user != visited_user:

        if not check_followship(login_user, visited_user):
            follow = Followship(
                initiative_user = login_user,
                followed_user = visited_user,
            )
            follow.save()
            notify.notify_follow(login_user, visited_user)
    return redirect('profile', username=username)

@login_required
def unfollow(request, username):
    login_user = request.user
    visited_user = User.objects.get(username=username)

    if login_user != visited_user:
        if check_followship(login_user, visited_user):
            followship = Followship.objects.get(
                initiative_user=login_user,
                followed_user=visited_user,
            )
            followship.delete()
    return redirect('profile', username=username)

# TODO
def explore(request):
    user_list = User.objects.all()
    tweet_list = []
    tweets = []
    if user_list:
        for user in user_list:
            if user.tweet_set.all():
                tweet_list.append(user.tweet_set.all()[0])
    paginate_by = 10
    tweets, show_pagination = share.pagination(request, tweet_list, paginate_by)
    return render(request, 'twitter/explore.html', {
        'tweets': tweets,
        'show_pagination': show_pagination,
    })