from atl_pahomqtt import CarriotsMqttClient
auth = {'username': 'e60ed329b656fa6d918f058af650a6de26a38b0697b7cf61ab204730cca3a53a', 'password': ''}
client_mqtt_post = CarriotsMqttClient(auth)
client_mqtt_post.post_to_carriots('{"foo":"foo1"}')
