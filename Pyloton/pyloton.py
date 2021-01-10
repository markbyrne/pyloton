#! /usr/bin/env python3.9
# -*- coding: latin-1 -*-

import requests
import json
import os
from Pyloton.version import __version__

VERBOSE = False
_BASE_URL = 'https://api.onepeloton.com'
_USER_AGENT = "pyloton/{}".format(__version__)
_HEADERS = {
	"Content-Type": "application/json",
	"User-Agent":   _USER_AGENT
}
_PELOTON_USERNAME = os.environ.get("PELOTON_USERNAME")
_PELOTON_PASSWORD = os.environ.get("PELOTON_PASSWORD")
_LOGGED_IN_USER = None
_SESSION = requests.Session()


class _UserObject:
	""" User Object. Created after login

    :type user_response: json
    """

	def __init__(self, user_response: dict):
		self.json = user_response
		if VERBOSE:
			print("_UserObject: ")
			print_json(self.json)
		self.session_id = user_response['session_id']
		self.user_data = _UserData(user_response['user_data'])
		self.user_id = user_response['user_id']


class _UserData:
	def __init__(self, user_data: dict):
		"""

        :type user_data: dict
        """
		self.json = user_data
		if VERBOSE:
			print("_UserData: ")
			print_json(self.json)
		self.allow_marketing = user_data['allow_marketing']
		self.birthday = user_data['birthday']
		self.block_explicit = user_data['block_explicit']
		self.can_charge = user_data['can_charge']
		self.birthday = user_data['birthday']
		self.contract_agreements = []
		for contract_agreement in user_data['contract_agreements']:
			self.contract_agreements.append(_UserContractAgreement(contract_agreement))
		self.created_at = user_data['created_at']
		self.created_country = user_data['created_country']
		self.customized_heart_rate_zones = _HeartRateZones(user_data['customized_heart_rate_zones'])
		self.customized_max_heart_rate = user_data['customized_max_heart_rate']
		self.cycling_ftp = user_data['cycling_ftp']
		self.cycling_ftp_source = user_data['cycling_ftp_source']
		self.cycling_ftp_workout_id = user_data['cycling_ftp_workout_id']
		self.cycling_workout_ftp = user_data['cycling_workout_ftp']
		self.default_heart_rate_zones = _HeartRateZones(user_data['default_heart_rate_zones'])
		self.default_max_heart_rate = user_data['default_max_heart_rate']
		self.email = user_data['email']
		self.estimated_cycling_ftp = user_data['estimated_cycling_ftp']
		self.facebook_access_token = user_data['facebook_access_token']
		self.facebook_id = user_data['facebook_id']
		self.first_name = user_data['first_name']
		self.gender = user_data['gender']
		self.has_active_device_subscription = user_data['has_active_device_subscription']
		self.has_active_digital_subscription = user_data['has_active_digital_subscription']
		self.has_signed_waiver = user_data['has_signed_waiver']
		self.height = user_data['height']
		self.id = user_data['id']
		self.image_url = user_data['image_url']
		self.instructor_id = user_data['instructor_id']
		self.is_complete_profile = user_data['is_complete_profile']
		self.is_demo = user_data['is_demo']
		self.is_external_beta_tester = user_data['is_external_beta_tester']
		self.is_fitbit_authenticated = user_data['is_fitbit_authenticated']
		self.is_internal_beta_tester = user_data['is_internal_beta_tester']
		self.is_profile_private = user_data['is_profile_private']
		self.is_provisional = user_data['is_provisional']
		self.is_strava_authenticated = user_data['is_strava_authenticated']
		self.last_name = user_data['last_name']
		self.last_workout_at = user_data['last_workout_at']
		self.location = user_data['location']
		self.member_groups = user_data['member_groups']  # TODO member group object
		self.middle_initial = user_data['middle_initial']
		self.name = user_data['name']
		self.obfuscated_email = user_data['obfuscated_email']
		self.paired_devices = []
		for paired_device in user_data['paired_devices']:
			self.paired_devices.append(_PairedDevice(paired_device))
		self.phone_number = user_data['phone_number']
		self.quick_hits = user_data['quick_hits']  # TODO quick_hits object
		self.referral_code = user_data['referral_code']
		self.referrals_made = user_data['referrals_made']
		self.subscription_credits = user_data['subscription_credits']
		self.subscription_credits_used = user_data['subscription_credits_used']
		self.total_followers = user_data['total_followers']
		self.total_non_pedaling_metric_workouts = user_data['total_non_pedaling_metric_workouts']
		self.total_pedaling_metric_workouts = user_data['total_pedaling_metric_workouts']
		self.total_pending_followers = user_data['total_pending_followers']
		self.total_workouts = user_data['total_workouts']
		self.username = user_data['username']
		self.v1_referrals_made = user_data['v1_referrals_made']
		self.weight = user_data['weight']
		self.workout_counts = {}
		for workout in user_data['workout_counts']:
			self.workout_counts[workout['name']] = _WorkoutCount(workout)


class _WorkoutCount:
	def __init__(self, workout_counts_data: dict):
		"""

        :type workout_counts_data: dict
        """
		self.json = workout_counts_data
		self.name = workout_counts_data['name']
		self.count = workout_counts_data['count']
		self.icon_url = workout_counts_data['icon_url']
		self.slug = workout_counts_data['slug']


class _PairedDevice:
	def __init__(self, paired_device_data: dict):
		"""

        :type paired_device_data: dict
        """
		self.json = paired_device_data
		self.name = paired_device_data['name']
		self.paired_device_type = paired_device_data['paired_device_type']
		self.serial_number = paired_device_data['serial_number']


class _HeartRateZones:
	def __init__(self, heart_rate_zones_data: dict):
		"""

        :type heartratezones_data: dict
        """
		self.list = heart_rate_zones_data
		self.zone_1 = heart_rate_zones_data[0] if heart_rate_zones_data else None
		self.zone_2 = heart_rate_zones_data[1] if heart_rate_zones_data else None
		self.zone_3 = heart_rate_zones_data[2] if heart_rate_zones_data else None
		self.zone_4 = heart_rate_zones_data[3] if heart_rate_zones_data else None
		self.zone_5 = heart_rate_zones_data[4] if heart_rate_zones_data else None

	def toJSON(self) -> dict:
		json = {
			'Zone_1': self.zone_1,
			'Zone_2': self.zone_2,
			'Zone_3': self.zone_3,
			'Zone_4': self.zone_4,
			'Zone_5': self.zone_5,
		}
		return json


class _UserContractAgreement:
	def __init__(self, contract_agreement_data: dict):
		"""

        :type user_data: dict
        """
		self.json = contract_agreement_data
		self.agreed_at = contract_agreement_data['agreed_at']
		self.bike_contract_url = contract_agreement_data['bike_contract_url']
		self.contract_created_at = contract_agreement_data['contract_created_at']
		self.contract_display_name = contract_agreement_data['contract_display_name']
		self.contract_id = contract_agreement_data['contract_id']
		self.contract_type = contract_agreement_data['contract_type']
		self.tread_contract_url = contract_agreement_data['tread_contract_url']


class _LiveClassResponse:
	def __init__(self, live_class_response_data: dict):
		self.json = live_class_response_data
		self.browse_categories = []
		for browse_category_data in live_class_response_data["browse_categories"]:
			self.browse_categories.append(_BrowseCategories(browse_category_data))
		self.class_types = []
		for class_type_data in live_class_response_data["class_types"]:
			self.class_types.append(_ClassType(class_type_data))
		self.count = live_class_response_data["count"]
		self.live_classes = []
		for live_class_data in live_class_response_data["data"]:
			self.live_classes.append(_LiveClass(live_class_data))
		self.equipment = []
		for equipment_data in live_class_response_data["equipment"]:
			self.equipment.append(_Equipment(equipment_data))
		self.limit = live_class_response_data["limit"]
		self.ride_types = []
		self.instructors = []
		for instructor in live_class_response_data["instructors"]:
			self.instructors.append(_Instructor(instructor))
		for ride_type_data in live_class_response_data["ride_types"]:
			self.ride_types.append(_RideType(ride_type_data))
		self.rides = []
		for ride_data in live_class_response_data["rides"]:
			self.rides.append(_Ride(ride_data))
		self.sort_by = live_class_response_data["sort_by"]
		self.total = live_class_response_data["total"]


class _Ride:
	def __init__(self, ride_data: dict):
		self.json = ride_data
		self.captions = ride_data["captions"]
		self.class_type_ids = ride_data["class_type_ids"]
		self.content_format = ride_data["content_format"]
		self.content_provider = ride_data["content_provider"]
		self.description = ride_data["description"]
		self.difficulty_estimate = ride_data["difficulty_estimate"]
		self.difficulty_level = ride_data["difficulty_level"]
		self.difficulty_rating_avg = ride_data["difficulty_rating_avg"]
		self.difficulty_rating_count = ride_data["difficulty_rating_count"]
		self.duration = ride_data["duration"]
		self.equipment_ids = ride_data["equipment_ids"]
		self.equipment_tags = ride_data["equipment_tags"]
		self.extra_images = ride_data["extra_images"]
		self.fitness_discipline = ride_data["fitness_discipline"]
		self.fitness_discipline_display_name = ride_data["fitness_discipline_display_name"]
		self.has_closed_captions = ride_data["has_closed_captions"]
		self.has_free_mode = ride_data["has_free_mode"]
		self.has_pedaling_metrics = ride_data["has_pedaling_metrics"]
		self.home_peloton_id = ride_data["home_peloton_id"]
		self.id = ride_data["id"]
		self.image_url = ride_data["image_url"]
		self.instructor_id = ride_data["instructor_id"]
		self.is_archived = ride_data["is_archived"]
		self.is_closed_caption_shown = ride_data["is_closed_caption_shown"]
		self.is_explicit = ride_data["is_explicit"]
		self.is_live_in_studio_only = ride_data["is_live_in_studio_only"]
		self.join_tokens = ride_data["join_tokens"]
		self.language = ride_data["language"]
		self.length = ride_data["length"]
		self.live_stream_id = ride_data["live_stream_id"]
		self.live_stream_url = ride_data["live_stream_url"]
		self.location = ride_data["location"]
		self.metrics = ride_data["metrics"]
		self.origin_locale = ride_data["origin_locale"]
		self.original_air_time = ride_data["original_air_time"]
		self.overall_estimate = ride_data["overall_estimate"]
		self.overall_rating_avg = ride_data["overall_rating_avg"]
		self.overall_rating_count = ride_data["overall_rating_count"]
		self.pedaling_duration = ride_data["pedaling_duration"]
		self.pedaling_end_offset = ride_data["pedaling_end_offset"]
		self.pedaling_start_offset = ride_data["pedaling_start_offset"]
		self.rating = ride_data["rating"]
		self.ride_type_id = ride_data["ride_type_id"]
		self.ride_type_ids = ride_data["ride_type_ids"]
		self.sample_vod_stream_url = ride_data["sample_vod_stream_url"]
		self.scheduled_start_time = ride_data["scheduled_start_time"]
		self.series_id = ride_data["series_id"]
		self.sold_out = ride_data["sold_out"]
		self.studio_peloton_id = ride_data["studio_peloton_id"]
		self.title = ride_data["title"]
		self.total_in_progress_workouts = ride_data["total_in_progress_workouts"]
		self.total_ratings = ride_data["total_ratings"]
		self.total_workouts = ride_data["total_workouts"]
		self.vod_stream_id = ride_data["vod_stream_id"]
		self.vod_stream_url = ride_data["vod_stream_url"]


class _RideType:
	def __init__(self, ride_type_data: dict):
		self.json = ride_type_data
		self.display_name = ride_type_data["display_name"]
		self.fitness_discipline = ride_type_data["fitness_discipline"]
		self.id = ride_type_data["id"]
		self.is_active = ride_type_data["is_active"]
		self.list_order = ride_type_data["list_order"]
		self.name = ride_type_data["name"]


class _LiveClass:
	def __init__(self, live_class_data: dict):
		self.json = live_class_data
		self.authed_user_reservation_id = live_class_data["authed_user_reservation_id"]
		self.countdown = live_class_data["countdown"]
		self.created_at = live_class_data["created_at"]
		self.end_time = live_class_data["end_time"]
		self.id = live_class_data["id"]
		self.is_complete = live_class_data["is_complete"]
		self.is_encore = live_class_data["is_encore"]
		self.is_live = live_class_data["is_live"]
		self.is_session = live_class_data["is_session"]
		self.is_studio = live_class_data["is_studio"]
		self.join_token = live_class_data["join_token"]
		self.pedaling_end_time = live_class_data["pedaling_end_time"]
		self.pedaling_start_time = live_class_data["pedaling_start_time"]
		self.ride_id = live_class_data["ride_id"]
		self.scheduled_start_time = live_class_data["scheduled_start_time"]
		self.seconds_since_start = live_class_data["seconds_since_start"]
		self.server_time = live_class_data["server_time"]
		self.start_time = live_class_data["start_time"]
		self.status = live_class_data["status"]
		self.total_home_reservations = live_class_data["total_home_reservations"]
		self.total_workouts = live_class_data["total_workouts"]


class _Equipment:
	def __init__(self, equipment_data: dict):
		self.json = equipment_data
		self.icon_url = equipment_data['icon_url']
		self.id = equipment_data['id']
		self.name = equipment_data['name']
		self.slug = equipment_data['slug']


class _FitnessDiscipline:
	def __init__(self, fitness_disciplines_data: dict):
		self.json = fitness_disciplines_data
		self.name = fitness_disciplines_data['name']
		self.id = fitness_disciplines_data['id']


class _Instructor:
	def __init__(self, instructor_data: dict):
		self.json = instructor_data
		self.about_image_url = instructor_data['about_image_url']
		self.background = instructor_data['background']
		self.bike_instructor_list_display_image_url = instructor_data['bike_instructor_list_display_image_url']
		self.bio = instructor_data['bio']
		self.coach_type = instructor_data['coach_type']
		self.facebook_fan_page = instructor_data['facebook_fan_page']
		self.featured_profile = instructor_data['featured_profile']
		self.film_link = instructor_data['film_link']
		self.first_name = instructor_data['first_name']
		self.fitness_disciplines = instructor_data['fitness_disciplines']
		self.id = instructor_data['id']
		self.image_url = instructor_data['image_url']
		self.instagram_profile = instructor_data['instagram_profile']
		self.instructor_hero_image_url = instructor_data['instructor_hero_image_url']
		self.ios_instructor_list_display_image_url = instructor_data['ios_instructor_list_display_image_url']
		self.is_filterable = instructor_data['is_filterable']
		self.is_instructor_group = instructor_data['is_instructor_group']
		self.is_visible = instructor_data['is_visible']
		self.jumbotron_url = instructor_data['jumbotron_url']
		self.jumbotron_url_dark = instructor_data['jumbotron_url_dark']
		self.jumbotron_url_ios = instructor_data['jumbotron_url_ios']
		self.last_name = instructor_data['last_name']
		self.life_style_image_url = instructor_data['life_style_image_url']
		self.list_order = instructor_data['list_order']
		self.music_bio = instructor_data['music_bio']
		self.name = instructor_data['name']
		self.ordered_q_and_as = []
		for q_and_a in instructor_data['ordered_q_and_as']:
			self.ordered_q_and_as.append(_Q_and_A(q_and_a))
		self.quote = instructor_data['quote']
		self.short_bio = instructor_data['short_bio']
		self.spotify_playlist_uri = instructor_data['spotify_playlist_uri']
		self.strava_profile = instructor_data['strava_profile']
		self.twitter_profile = instructor_data['twitter_profile']
		self.user_id = instructor_data['user_id']
		self.username = instructor_data['username']
		self.web_instructor_list_display_image_url = instructor_data['web_instructor_list_display_image_url']
		self.web_instructor_list_gif_image_url = instructor_data['web_instructor_list_gif_image_url']
		self.workout_share_images = instructor_data['workout_share_images']  # TODO workout_share_images object


class _Q_and_A:
	def __init__(self, Q_and_A_list: list):
		self.list = Q_and_A_list
		self.question = Q_and_A_list[0]
		self.answer = Q_and_A_list[1]


class _BrowseCategories:
	def __init__(self, browse_categories_data: dict):
		self.json = browse_categories_data
		self.icon_url = browse_categories_data["icon_url"]
		self.id = browse_categories_data["id"]
		self.list_order = browse_categories_data["list_order"]
		self.name = browse_categories_data["name"]
		self.portal_image_url = browse_categories_data["portal_image_url"]
		self.slug = browse_categories_data["slug"]


class _ClassType:
	def __init__(self, class_types_data: dict):
		self.json = class_types_data
		self.display_name = class_types_data["display_name"]
		self.fitness_discipline = class_types_data["fitness_discipline"]
		self.id = class_types_data["id"]
		self.is_active = class_types_data["is_active"]
		self.list_order = class_types_data["list_order"]
		self.name = class_types_data["name"]


def print_json(obj):
	json_str = json.dumps(obj, sort_keys=True, indent=4)
	print(json_str)


def log_in_user(username_or_email=None, password=None):
	payload = None
	if (username_or_email is None) or (password is None):
		payload = {'username_or_email': _PELOTON_USERNAME, 'password': _PELOTON_PASSWORD}
	else:
		payload = {'username_or_email': username_or_email, 'password': password}
	response = _SESSION.post(_BASE_URL + '/auth/login', json=payload, headers=_HEADERS)
	_LOGGED_IN_USER = _UserObject(response.json())


def get_resgistered_classes() -> ([_LiveClass], _LiveClassResponse):
	'''
    Returns the a list of _LiveClass objects that the signed-in User has registered to attend ("Counted In") and a _LiveClassResponse object that is effectively a Live Classes catalog,
    which you can use to get ride and instructor information from for the registered rides without needing to make a second API call.

    Parameters:


    Returns:
        registered_classes: A list of classes that the signed-in user has registered for.
        live_classes_catelog: Object containing a catalog of information including Instructor and Ride information
    '''

	if _LOGGED_IN_USER is None:
		log_in_user()

	live_classes_catalog = get_live_classes()

	registered_classes = []
	for live_class in live_classes_catalog.live_classes:
		if live_class.authed_user_reservation_id:
			registered_classes.append(live_class)

	return registered_classes, live_classes_catalog


def get_ride(ride_id) -> _Ride:
	class_response = _SESSION.get(_BASE_URL + '/api/ride/' + ride_id)
	class_json_response = class_response.json()
	return _Ride(class_json_response)


def get_instructor(instructor_id) -> _Instructor:
	instructor_response = _SESSION.get(_BASE_URL + '/api/instructor/' + instructor_id)
	instructor_json_response = instructor_response.json()
	return _Instructor(instructor_json_response)


def get_instructors() -> [_Instructor]:
	instructor_response = _SESSION.get(_BASE_URL + '/api/instructor/')
	instructor_json_response = instructor_response.json()
	instructors = []
	for instructor_data in instructor_json_response["data"]:
		instructors.append(_Instructor(instructor_data))
	return instructors


def get_live_classes(exclude_complete='true', exclude_live_in_studio_only='true') -> _LiveClassResponse:
	params = {
		'exclude_complete':            exclude_complete,
		'exclude_live_in_studio_only': exclude_live_in_studio_only
	}
	response = _SESSION.get(_BASE_URL + '/api/v3/ride/live', params=params)
	json_response = response.json()

	if VERBOSE:
		print_json(json_response)

	return _LiveClassResponse(json_response)


if __name__ == '__main__':
	pass
