from app.core import read_json
from pycoingecko import CoinGeckoAPI

words = read_json.ReadJson()
cg = CoinGeckoAPI()


class Rpos:
    def __init__(self):
        pass

    def head_foot(self):
        head_foot_context = {
            "nav_list": words.read_nav_home_words(),
            "footer_list": enumerate(words.read_footer_home()),
        }
        return head_foot_context

    def url_silde(self, api, id):

        urls = {
            "url_home": api+"home",
            "url_projects": api+"users/"+str(id)+"/project",
            "url_profile": api+"users/"+str(id)+"/profile",
            "url_about_us": api+"about-us",
            "url_privacy": api+"privacy",
            "url_wallet": api+"users/"+str(id)+"/wallet"
        }
        return urls

    def tabs_headers(self):
        tabs = {
            "funder": words.read_tabs_headers()[0],
            "lancer": words.read_tabs_headers()[1],
        }
        return tabs

    def coin_prices(self):
        price = cg.get_price(ids='ombre', vs_currencies='usd')
        prices = {
            "omb_price": price["ombre"]["usd"]
        }
        # prices = {
        #     "omb_price": 1
        # }
        return prices

    def get_context_home(self):
        context_home = {
            "title": words.read_title_home_word(),
            "nav_list": words.read_nav_home_words(),
            "image_list": words.read_addr_home_images(),
            "des_list": words.read_description_home_sences(),
            "footer_list": enumerate(words.read_footer_home()),
            "sign_in_url": words.read_signin_url(),
            "sign_up_url": words.read_signup_url()
        }
        return context_home
    def get_contex_login(self):
        context_login = {
            "title": words.read_title_signin_word(),
            "nav_list": words.read_nav_home_words(),
            "footer_list": enumerate(words.read_footer_home()),
            "input_list": words.read_input_signin_words(),
            "sign_in_url": words.read_signin_url(),
            "sign_up_url": words.read_signup_url()
        }
        return context_login
    def get_context_signup(self):
        context_sign_up ={
            "nav_list": words.read_nav_home_words(),
            "footer_list": enumerate(words.read_footer_home()),
            "title": words.read_title_signup_word(),
            "input_list":words.read_input_signup_words(),
            "sign_in_url": words.read_signin_url(),
            "sign_up_url": words.read_signup_url()
        }
        return context_sign_up
    def get_context_profile(self, api, id):
        context_profile = {
            "title": words.read_title_of_profile(),
            "label_fname": words.read_profile_fname(),
            "label_lname": words.read_profile_lname(),
            "label_burn": words.read_profile_burn(),
            "label_resume": words.read_profile_resume(),
            "label_owa": words.read_profile_wa(),
            "label_bio": words.read_profile_bio(),
            "label_address": words.read_profile_addr(),
            "label_city": words.read_profile_city(),
            "label_country": words.read_profile_country(),
            "title_project_developed": words.read_profile_final_proj_dev_title(),
            "title_project_developing": words.read_profile_proj_dev_title(),
            "title_project_define": words.read_profile_proj_def_title(),
            "title_project_define_and_developed": words.read_profile_proj_fin_def_title(),
            "NAME": words.read_profile_name(),
            "START_DATE": words.read_profile_start_date(),
            "END_DATE": words.read_profile_end_date(),
            "DESCRIBE": words.read_profile_describe(),
            "COST": words.read_profile_cost(),
            "omb_price": 1,
            "total": 1,
            "page": 1
        }
        context_profile.update(self.tabs_headers())
        context_profile.update(self.head_foot())
        context_profile.update(self.url_silde(api=api, id=id))
        return context_profile

    def get_context_project(self, api, id):
        context_profile = {
            "title": words.read_title_of_project(),
            "label_name": words.read_name_of_project_lancer(),
            "label_description": words.read_description_of_project_lancer(),
            "label_deadline": words.read_deadline_of_project_lancer(),
            "label_file": words.read_file_of_project_lancer(),
            "label_usd_cost": words.read_cost_of_project_lancer(),
            "label_img": words.read_img_of_project_lancer(),
            "label_omb_cost": words.read_cost_of_project_lancer(),
            "NAME": words.read_item_project_name(),
            "COST": words.read_cost_of_project_lancer(),
            "DEAD_LINE": words.read_deadline_of_project_lancer()
        }
        context_profile.update(self.head_foot())
        context_profile.update(self.url_silde(api=api, id=id))
        context_profile.update(self.tabs_headers())
        context_profile.update(self.coin_prices())
        return context_profile

    def get_context_upload_project(self, api, id):
        context_profile = {
            "title": words.read_title_of_upload_project_page(),
            "upload_project": words.read_placeholder_of_upload_project_page(),
            "submit": words.read_submit_of_upload_project_page(),
            "omb_price": 1,
            "total": 1,
            "page": 1
        }
        context_profile.update(self.head_foot())
        context_profile.update(self.url_silde(api=api, id=id))
        return context_profile

    def get_context_accept_project(self, api, id):
        context_profile = {
            "title": words.read_present_project_title(),
            "submit": words.read_submit_of_present_project_page(),
            "common_desc": words.read_common_of_present_project_page(),
            "download": words.read_download_of_present_project_page(),
            "omb_price": 1,
            "total": 1,
            "page": 1
        }
        context_profile.update(self.head_foot())
        context_profile.update(self.url_silde(api=api, id=id))
        return context_profile

    def get_context_wallet(self, api, id):
        context_wallet = {
            "title": words.read_ombre_title(),
            "rec_addr": words.read_ombre_recieve_address(),
            "submit": words.read_submit_of_upload_project_page(),
            "enter_addr": words.read_ombre_recieve_address_enter(),
            "amount": words.read_ombre_amount(),
            "enter_amount": words.read_ombre_amount_enter(),
            "omb_price": 1,
            "total": 1,
            "page": 1
        }
        context_wallet.update(self.head_foot())
        context_wallet.update(self.url_silde(api=api, id=id))
        return context_wallet