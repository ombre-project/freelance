import json
import os

class ReadJson():
    """
    this class use to read values need allover project from values.json file
    """
    def __init__(self):
        file = open(os.getcwd()+'/values.json', "r")
        fj = json.loads(file.read())
        self.fj_lang = fj["en"]
        file.close()

    def read_project_name(self):
        """
        this method get name of project
        :return: a value from values.json file
        :rtype: str
        """
        return self.fj_lang["PROJECT_NAME"]
    def read_server_name(self):
        """
        this method get name of server
        :return: a value from values.json file
        :rtype: str
        """
        return self.fj_lang["SERVER_NAME"]
    def read_server_host(self):
        """
        this method get name of server host
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["SERVER_HOST"]
    def read_sentry_dns(self):
        """
        this method get the sentry dns
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["SENTRY_DNS"]
    def read_postgres_server(self):
        """
        this method get name of postgres server
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["POSTGRES_SERVER"]
    def read_postgres_user(self):
        """
        this method get name of postgres user
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["POSTGRES_USER"]
    def read_postgres_password(self):
        """
        this method get the postgres password
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["POSTGRES_PASSWORD"]
    def read_postgres_db(self):
        """
        this method get the postgres db name
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["POSTGRES_DB"]
    def read_postgres_uri(self):
        """
        this method get the postgres url
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["POSTGRES_URI"]
    def read_nav_home_words(self):
        """
        this method get list of words they use in navigation bar
        :return: list os values from values.json file
        :rtype: list
        """

        return self.fj_lang["HOME_PAGE"]["NAVIGATION_BAR"]
    def read_title_home_word(self):
        """
        this method get the title of home page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["HOME_PAGE"]["TITLE"]
    def read_addr_home_images(self):
        """
        this method get the address of images use in home page
        :return: list of values from values.json file
        :rtype: list
        """

        return self.fj_lang["HOME_PAGE"]["IMAGES"]
    def read_description_home_sences(self):
        """
        this method get some text use in home page ui
        :return: list of values from values.json file
        :rtype: list
        """

        return self.fj_lang["HOME_PAGE"]["DESCRIPTIONS"]
    def read_comment_home_cards(self):
        """
        this method get values use in cards in home page ui
        :return: 3 lists of values from values.json file
        :rtype: 3 lists
        """

        return self.fj_lang["HOME_PAGE"]["IMAGES_COMMENT"], self.fj_lang["HOME_PAGE"]["NAMES_COMMENT"], self.fj_lang["HOME_PAGE"]["DESCRIPTIONS_COMMENT"]
    def read_footer_home(self):
        """
        this method get values use in footer of home page
        :return: list of values from values.json file
        :rtype: list
        """

        return self.fj_lang["HOME_PAGE"]["FOOTER"]
    def read_title_signup_word(self):
        """
        this method get title use in sign up page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["SIGNUP"]["TITLE"]
    def read_input_signup_words(self):
        """
        this method get some values use in sign up page
        :return: list of values from values.json file
        :rtype: list
        """

        return self.fj_lang["SIGNUP"]["INPUT_LIST"]
    def read_signin_url(self):
        """
        this method get sign in url
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["SIGNIN_URL"]
    def read_signup_url(self):
        """
        this method get sign up url
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["SIGNUP_URL"]
    def read_home_url(self):
        """
        this method get home url
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["HOME_URL"]
    def read_title_signin_word(self):
        """
        this method get title of login page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["LOGIN"]["TITLE"]
    def read_input_signin_words(self):
        """
        this method get some values use in login ui page
        :return: list of values from values.json file
        :rtype: list
        """

        return self.fj_lang["LOGIN"]["INPUT_LIST"]
    def read_title_of_profile(self):
        """
        this method get title of profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["TITLE"]
    def read_profile_fname(self):
        """
        this method get first name tag use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["FNAME"]
    def read_profile_lname(self):
        """
        this method get last name tag use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["LNAME"]
    def read_profile_resume(self):
        """
        this method get resume tag use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["RESUME"]
    def read_profile_burn(self):
        """
        this method get burn date tag use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["BURN"]
    def read_profile_wa(self):
        """
        this method get wallet address tag use in profile page
        :return: a value from values.json file
        :rtype: str
        """


        return self.fj_lang["PROFILE"]["WALLETADDRESS"]
    def read_profile_bio(self):
        """
        this method get bio tag that use in profile page
        :return: a value from values.json file
        :rtype: str
        """


        return self.fj_lang["PROFILE"]["BIO"]
    def read_profile_addr(self):
        """
        this method get address tag that use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["ADDRESS"]
    def read_profile_city(self):
        """
        this method get city tag that use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["CITY"]
    def read_profile_country(self):
        """
        this method get country tag that use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["COUNTRY"]
    def read_profile_img_prof(self):
        """
        this method get image address use in profile ui client to load an image
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["IMGADDRESS"]
    def read_profile_final_proj_dev_title(self):
        """
        this method get a title use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["FINAL_PROJECT_DEVELOPED"]
    def read_profile_name(self):
        """
        this method get name tag that use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["NAME"]
    def read_profile_start_date(self):
        """
        this method get start date tag that use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["START_DATE"]
    def read_profile_cost(self):
        """
        this method get cost tag that use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["COST"]
    def read_profile_end_date(self):
        """
        this method get end date label that use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["END_DATE"]
    def read_profile_describe(self):
        """
        this method get description label that use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["DESCRIBE"]
    def read_profile_proj_dev_title(self):
        """
        this method get a text label use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["PROJECTS_ARE_DEVELOPING"]
    def read_profile_proj_def_title(self):
        """
        this method get a text label use in profile page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROFILE"]["PROJECT_DEFINED"]
    def read_profile_proj_fin_def_title(self):
        """
        this method get a text label use in profile page
        :return: a value from values.json file
        :rtype: str
        """
        return self.fj_lang["PROFILE"]["FINAL_PROJECT_DEFINED"]
    def read_title_of_project(self):
        """
        this method get title of project page
        :return: a value from values.json file
        :rtype: str
        """
        return self.fj_lang["PROJECT"]["TITLE"]
    def read_api_prev_url(self):
        """
        this method get prev url /api/v1/
        :return: a value from values.json file
        :rtype: str
        """
        return self.fj_lang["API_PREV_URL"]
    def read_tabs_headers(self):
        """
        this method get two word use in tab layout of ui
        :return: list of values from values.json file
        :rtype: list
        """
        return self.fj_lang["PROJECT"]["TABSHEADERS"]
    def read_name_of_project_lancer(self):
        """
        this method get name label use in project page
        :return: a value from values.json file
        :rtype: str
        """
        return self.fj_lang["PROJECT"]["NAME_LANCER"]
    def read_description_of_project_lancer(self):
        """
        this method get description label use in project page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROJECT"]["DESCRIPTION_LANCER"]
    def read_deadline_of_project_lancer(self):
        """
        this method get end date label use in project page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROJECT"]["DATE_FINISH_LANCER"]
    def read_file_of_project_lancer(self):
        """
        this method get file label use in project page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROJECT"]["FILE_LANCER"]
    def read_cost_of_project_lancer(self):
        """
        this method get cost label use in project page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROJECT"]["COST_LANCER"]
    def read_img_of_project_lancer(self):
        """
        this method get image label use in project page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROJECT"]["IMG_LANCER"]
    def read_item_project_name(self):
        """
        this method get name label use in project page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROJECT"]["NAME"]
    def read_item_project_end_date(self):
        """
        this method get end date label use in project page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROJECT"]["EDATE"]
    def read_item_project_cost(self):
        """
        this method get cost label use in project page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PROJECT"]["COST"]
    def read_title_of_upload_project_page(self):
        """
        this method get title of upload page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["UPLOAD"]["TITLE"]
    def read_placeholder_of_upload_project_page(self):
        """
        this method get a label use in upload page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["UPLOAD"]["UPLOAD_PROJECT"]
    def read_submit_of_upload_project_page(self):
        """
        this method get submit label use in upload page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["UPLOAD"]["SUBMIT"]
    def read_present_project_title(self):
        """
        this method get title use in present project page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PRESENT_PROJECT"]["TITLE"]
    def read_submit_of_present_project_page(self):
        """
        this method get submit label use in present project page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PRESENT_PROJECT"]["SUBMIT"]
    def read_common_of_present_project_page(self):
        """
        this method get common label use in present project page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PRESENT_PROJECT"]["COMMON"]
    def read_download_of_present_project_page(self):
        """
        this method get download label use in present project page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["PRESENT_PROJECT"]["DOWNLOAD"]
    def read_ombre_ip(self):
        """
        this method get ip of ombre node to connect to it
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["OMBRE"]["IP"]
    def read_ombre_port(self):
        """
        this method get port of ombre node to connect to it
        :return: a value from values.json file
        :rtype: int
        """

        return self.fj_lang["OMBRE"]["PORT"]
    def read_ombre_wallet_address(self):
        """
        this method get wallet address label use in wallet page
        :return: a value from values.json file
        :rtype: str
        """

        return self.fj_lang["OMBRE"]["WALLET_ADDRESS"]
    def read_ombre_balance(self):
        """
        this method get balance of account label use in wallet page
        :return: a value from values.json file
        :rtype: str
        """
        return self.fj_lang["OMBRE"]["BALANCE"]
    def read_ombre_title(self):
        """
        this method get title use in wallet page
        :return: a value from values.json file
        :rtype: str
        """
        return self.fj_lang["OMBRE"]["TITLE"]
    def read_ombre_recieve_address(self):
        """
        this method get receiver address label use in wallet page
        :return: a value from values.json file
        :rtype: str
        """
        return self.fj_lang["OMBRE"]["REC_ADDR"]
    def read_ombre_recieve_address_enter(self):
        """
        this method get enter wallet address label use in wallet page
        :return: a value from values.json file
        :rtype: str
        """
        return self.fj_lang["OMBRE"]["ENTER_REC_ADDR"]
    def read_ombre_amount(self):
        """
        this method get amount label use in wallet page
        :return: a value from values.json file
        :rtype: str
        """
        return self.fj_lang["OMBRE"]["AMOUNT"]
    def read_ombre_amount_enter(self):
        """
        this method get enter amount label use in wallet page
        :return: a value from values.json file
        :rtype: str
        """
        return self.fj_lang["OMBRE"]["ENTER_AMOUNT"]