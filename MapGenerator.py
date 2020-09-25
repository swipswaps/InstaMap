import branca
import getpass
import time
from folium import Map, Marker, Popup
from InstaScraper import create_location_dict, create_posts_object


print("Instagram has strict requests limit, please don't use the same Instagram profile in parallel "
      "during the execution of this script")
time.sleep(3)
print("In order to receive locations of posts you should sign into Instagram account (required by Instagram), "
      "otherwise locations would be None")
time.sleep(3)
username = input('Enter your username: ')
password = getpass.getpass(prompt='Enter your password: ')
profile_name = input('Enter target profile name: ')

posts_object = create_posts_object(profile_name, username, password)
print("Received posts object: ", posts_object)
time.sleep(1)
print("Please, wait until the current program is finished")
time.sleep(1)

# Create location_dict
t = time.time()
location_dict = create_location_dict(posts_object)
print("Done in: ", time.time()-t)


# Create map object
my_map = Map(location=[50.3005988, 24.2444963])
tooltip = 'Click here'

# put the data from Instagram profile on the map
for location in location_dict:
    try:
        html = '<head><style> div{display: block; text-align: center;} </style></head>'
        for post_tuple in location_dict[location]:
            date = post_tuple[0].date()
            url = post_tuple[1]
            post_url = 'http://www.instagram.com/p/' + post_tuple[3]
            likes = post_tuple[2]
            html += f"""
                    <div><strong>{date}</strong><br>
                    <a href="{post_url}" target='popup'><img src="{url}" width=150></a><br>
                    {likes} &#128077<br><br></div>
                    """
        # Creating IFrame object. It allows us to render html code for popup elements instead of using
        # default popup's design
        iframe = branca.element.IFrame(html=html, width=180, height='100%')
        popup = Popup(iframe)
        Marker(location, popup=popup, tooltip=tooltip).add_to(my_map)
    except ValueError:
        continue


my_map.save('map.html')
