import pydeck as pdk

def create_map(data, radius, initial_view_state):
    farmers_market_layer = pdk.Layer(
        'ScatterplotLayer',
        data=data,
        get_position='[Longitude, Latitude]',
        get_color=(250, 0, 0, 160),
        get_radius=radius,
        pickable=True,
        tooltip=True
    )

    # Set up the view state
    view_state = pdk.ViewState(latitude=33.7490, longitude=-84.3880, zoom=10, pitch=0)

    # Render the map with all layers
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v11',
        initial_view_state=initial_view_state,
        layers=[farmers_market_layer],
        tooltip={
            "text": "{Name}\n{Location}",
            "style": {
                "color": "white",
                "backgroundColor": "black",
                "fontFamily": "Arial",
            }
        }
    )

    return map