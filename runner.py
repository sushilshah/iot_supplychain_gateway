#from atl_pahomqtt import CarriotsMqttClient
#auth = {'username': 'e60ed329b656fa6d918f058af650a6de26a38b0697b7cf61ab204730cca3a53a', 'password': ''}
#client_mqtt_post = CarriotsMqttClient(auth)
#client_mqtt_post.post_to_carriots('{"foo":"foo1"}')

from sfdc_utils import SFDCUtils
x = SFDCUtils()
payload = '{"ID__c":"110","SensorID__c":"100","Type__c":"chick1","Status__c":"Transit","ShippingTime__c":"2005-10-08T00:00:00Z"}'
print x.post(payload)
