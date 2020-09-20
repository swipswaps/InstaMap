from instaloader import Profile, Instaloader


def create_posts_object(profile_name, username, password):
    """
    In order to receive locations of posts we should sign into Instagram account (required by Instagram),
    otherwise locations would be None
    :param username: username;
    :param password: password;
    :param profile_name: the name of target profile;
    :return: posts object of Instaloader Profile class;
    """
    L = Instaloader()
    L.login(username, password)

    profile = Profile.from_username(L.context, profile_name)
    posts = profile.get_posts()

    return posts


def create_location_dict(posts_object):
    """
    :param posts_object: posts object of Instaloader Profile class;
    :return: dictionary where the keys are locations of the posts and value is list of tuples;
    Each tuple in this list is a sequence of post data (date, url, amount of likes etc.)
    """
    dictionary = {}
    count = 0
    for post in posts_object:
        try:
            loc_tuple = (post.location.lat, post.location.lng)
            if loc_tuple not in dictionary:
                dictionary[loc_tuple] = [(post.date, post.url, post.likes, post.shortcode)]
                count += 1
            else:
                dictionary[loc_tuple].append((post.date, post.url, post.likes, post.shortcode))
                count += 1
            print("Scraping", 'post number', count)
        except AttributeError:
            count += 1
            continue

        # # TEST CONDITION (for test purposes)
        # if count == 8:
        #     break
    return dictionary
