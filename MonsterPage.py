"""
    This is the MonsterPage module
"""

import json
import os
from ConsoleUtil import ConsoleUtil
from Rating import Rating
from MonsterType import MonsterType
from LinkType import LinkType

class MonsterPage():
    """
        This class represents the parsed result of a single monster
        page
    """

    DEFAULT_ELEMENT = MonsterType.FIRE
    __OVERVIEW_XPATH = '//*[@id="overview-anchor"]/div[2]/div[2]'

    @staticmethod
    def convert_element_to_link_type(element):
        """
            This method is used to convert from a MonsterType to
            a LinkType
        """
        if LinkType.has_value(element.value):
            return LinkType[element.value]
        return LinkType[MonsterPage.DEFAULT_ELEMENT.value]

    @staticmethod
    def load_from_disk(filepath):
        """
            This method attempts to parse and load a MonsterPage
            object from the disk according to the filepath passed in
        """
        data = {}
        new_mon = None
        with open(filepath, 'r') as in_file:
            data = json.load(in_file)
            new_mon = MonsterPage(tree=None, data=data)
        return new_mon

    @classmethod
    def __parse_single_score(cls, elem):
        """
            This method attempts to parse a score from an element
            passed in
        """
        raw_score = elem
        score_exists = len(elem) > 0
        score_result = 0

        if not score_exists:
            return score_result

        raw_score = raw_score[0] # store the target element
        score_has_children = len(raw_score) > 0

        if score_has_children:
            raw_score = raw_score[0].text # use child instead
        else:
            raw_score = raw_score.text

        try:
            score_result = float(raw_score.strip())
        except ValueError:
            pass

        return score_result

    @classmethod
    def __parse_alt_link_info(cls, anchor_node):
        """
            This method parses the URL and type of a particular element link
            on a monster page using xpath on a node
        """
        alt_type = MonsterPage.DEFAULT_ELEMENT
        href = anchor_node.attrib['href'].strip().replace('https:', '')
        title_exists = True

        try:
            title_attribute = anchor_node.attrib['title']
        except KeyError:
            title_exists = False

        if title_exists:
            href_type = title_attribute[0 : title_attribute.find(' ')].upper()
        else:
            start_ind = href.find('.co/') + 4
            end_ind = href.find('-', start_ind)
            href_type = href[start_ind : end_ind].upper()

        if MonsterType.has_value(href_type):
            alt_type = MonsterType[href_type]
        else:
            ConsoleUtil.warn(f'Got unexpected href_type="{href_type}"')

        return {
            'alt_link': href,
            'link_type': MonsterPage.convert_element_to_link_type(alt_type)
        }

    def print_mon_info(self):
        """
            This method prints out the basic information parsed from a MonsterPage
        """
        print('')
        print(f'Full Name: {self.full_name}')
        print(f'Sleepy Name: {self.sleepy_name}')
        print(f'Awakened Name: {self.awaken_name}')
        print(f'Element: {self.element}')
        print(f'Grade: {self.grade}')
        print(f'Grade Num: {self.grade_num}')
        print(f'Mon Type: {self.mon_type}')
        print(f'Get From: {self.get_from}')
        print(f'When Awakened: {self.when_awakened}')
        print(f'Good For: {self.good_for}')
        print(f'Skill Up Info: {self.skillup_info}')
        print(f'Total Score: {self.score_total}')
        print(f'User Score: {self.score_user}')
        print(f'Ratings: {self.ratings}')
        print(f'Links: {self.links}')

    def get_filepath(self):
        """
            This method will return a string filepath; this is used in
            conjunction with serialize
        """
        cwd = os.getcwd()
        no_left_parens = self.full_name.replace('(', '')
        no_parens = no_left_parens.replace(')', '')
        no_spaces = no_parens.replace(' ', '_').strip()
        lowered = no_spaces.lower()

        return f'{cwd}/data/mons/{lowered}.json'

    def deserialize(self, data):
        """
            This method takes a dict of values to initialize a MonsterPage
            object
        """
        self.element = MonsterType[data['element']]
        self.get_from = data['get_from']
        self.good_for = data['good_for']
        self.grade = data['grade']
        self.grade_num = data['grade_num']

        self.links = LinkType.generate_link_dict()

        for link_key in data['links']:
            self.links[LinkType[link_key]] = data['links'][link_key]

        self.mon_type = data['mon_type']
        self.awaken_name = data['name_awaken']
        self.full_name = data['name_full']
        self.sleepy_name = data['name_sleepy']

        self.ratings = Rating.generate_rating_dict()

        for rating_key in data['ratings']:
            self.ratings[Rating[rating_key]] = data['ratings'][rating_key]

        self.score_total = data['score_total']
        self.score_user = data['score_user']
        self.skillup_info = data['skillup_info']
        self.when_awakened = data['when_awaken']

    def serialize(self, filepath=''):
        """
            This method will attempt to write this instance of MonsterPage
            to a file, determined by the filepath param which defaults to
            using MonsterPage.get_filepath()
        """
        if filepath == '':
            filepath = self.get_filepath()

        mapped_links = {}
        mapped_ratings = {}

        for link_key in self.links:
            mapped_links[link_key.value] = self.links[link_key]

        for rating_key in self.ratings:
            mapped_ratings[rating_key.value] = self.ratings[rating_key]

        data = {
            'element': self.element.value,
            'get_from': self.get_from,
            'good_for': self.good_for,
            'grade': self.grade,
            'grade_num': self.grade_num,
            'links': mapped_links,
            'mon_type': self.mon_type,
            'name_awaken': self.awaken_name,
            'name_full': self.full_name,
            'name_sleepy': self.sleepy_name,
            'ratings': mapped_ratings,
            'score_total': self.score_total,
            'score_user': self.score_user,
            'skillup_info': self.skillup_info,
            'when_awaken': self.when_awakened
        }

        with open(filepath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=2)

    def __init__(self, tree=None, data=None):
        self.element = MonsterPage.DEFAULT_ELEMENT
        self.get_from = ''
        self.good_for = ''
        self.grade = ''
        self.grade_num = 0
        self.links = LinkType.generate_link_dict()
        self.mon_type = ''
        self.awaken_name = ''
        self.full_name = ''
        self.sleepy_name = ''
        self.ratings = Rating.generate_rating_dict()
        self.score_total = 0
        self.score_user = 0
        self.skillup_info = ''
        self.when_awakened = ''

        if data != None:
            self.deserialize(data)
        elif tree != None:
            self.__parse_tree(tree)

    def __parse_tree(self, tree):
        """
            This method calls all of the other parsing methods
        """
        self.__parse_name(tree)
        self.__parse_element(tree)
        self.__parse_grade(tree)
        self.__parse_mon_type(tree)
        self.__parse_get_from(tree)
        self.__parse_when_awakened(tree)
        self.__parse_good_for(tree)
        self.__parse_skillup_info(tree)
        self.__parse_alt_links(tree)
        self.__parse_scores(tree)
        self.__parse_ratings(tree)
        self.__parse_image_links(tree)

    def __parse_element(self, tree):
        """
            This method parses the element of the monster from a tree
        """
        raw_mon_name = tree.xpath('//h1[@class="main-title"]')[0].text
        raw_mon_name = raw_mon_name.strip()
        raw_mon_name = raw_mon_name.replace('’', '')
        first_space_ind = raw_mon_name.find(' ')
        potential_element = raw_mon_name[0 : first_space_ind].upper()

        self.element = MonsterPage.DEFAULT_ELEMENT

        if MonsterType.has_value(potential_element):
            self.element = MonsterType[potential_element]
        else:
            ConsoleUtil.warn(f'Error parsing element, got: "{potential_element}"')

    def __parse_name(self, tree):
        """
            This method parses a name (and sleepy and awakened) from a tree
        """
        raw_mon_name = tree.xpath('//h1[@class="main-title"]')[0].text
        raw_mon_name = raw_mon_name.strip()
        raw_mon_name = raw_mon_name.replace('’', '')
        self.full_name = raw_mon_name
        first_space_ind = raw_mon_name.find(' ')
        paren_ind = self.full_name.find('(')
        self.sleepy_name = self.full_name[first_space_ind + 1 : paren_ind - 1] # -1 for the space
        self.awaken_name = self.full_name[paren_ind + 1 : -1]

    def __parse_grade(self, tree):
        """
            This method parses a grade and grade_num from a tree
        """
        xpath_selector = self.__OVERVIEW_XPATH + '/div[1]/span[2]/p'
        raw_grade = tree.xpath(xpath_selector)[0].text
        self.grade = raw_grade
        self.grade_num = len(self.grade)

    def __parse_mon_type(self, tree):
        """
            This method parses the type of a monster from a tree
        """
        xpath_selector = self.__OVERVIEW_XPATH + '/div[2]/span[2]/p'
        raw_type = tree.xpath(xpath_selector)[0].text
        self.mon_type = raw_type

    def __parse_get_from(self, tree):
        """
            This method parses the get from of a monster from a tree
        """
        xpath_selector = self.__OVERVIEW_XPATH + '/div[3]/span[2]/p'
        raw_get_from = tree.xpath(xpath_selector)[0].text
        self.get_from = raw_get_from

    def __parse_when_awakened(self, tree):
        """
            This method parses the when awakened of a monster from a tree
        """
        xpath_selector = self.__OVERVIEW_XPATH + '/div[4]/span[2]/p'
        raw_when_awakened = tree.xpath(xpath_selector)[0].text
        self.when_awakened = raw_when_awakened

    def __parse_good_for(self, tree):
        """
            This method parses the good for of a monster from a tree
        """
        xpath_selector = self.__OVERVIEW_XPATH + '/div[5]/span[2]/p'
        raw_good_for = tree.xpath(xpath_selector)[0].text
        self.good_for = raw_good_for

    def __parse_skillup_info(self, tree):
        """
            This method parses the skillup info of a monster from a tree
        """
        xpath_selector = self.__OVERVIEW_XPATH + '/div[6]/span[2]/p'
        raw_skillup_info = tree.xpath(xpath_selector)[0].text
        self.skillup_info = raw_skillup_info

    def __parse_scores(self, tree):
        """
            This method parses a total and user score from a tree
        """
        xpath_rating = '//*[@id="rating-anchor"]'
        xpath_editor = '//*[contains(@class, "editor_rating")]'
        xpath_user = '//*[contains(@class, "user_rating")]'

        raw_score_total = tree.xpath(
            xpath_rating +
            xpath_editor +
            '/*[contains(@class, "number")]')
        raw_score_user = tree.xpath(
            xpath_rating +
            xpath_user +
            '/*[contains(@class, "number")]')

        self.score_total = self.__parse_single_score(raw_score_total)
        self.score_user = self.__parse_single_score(raw_score_user)

    def __parse_ratings(self, tree):
        """
            This method parses the ratings for a given monster from a tree
        """
        reaction_xpath = '//div[contains(@class,"reaction-percentage")]'

        raw_rating_keep = tree.xpath(reaction_xpath + "[contains(@class,'keep')]")[0].text
        raw_rating_food = tree.xpath(reaction_xpath + "[contains(@class,'food')]")[0].text
        raw_rating_best = tree.xpath(reaction_xpath + "[contains(@class,'best')]")[0].text
        raw_rating_meh = tree.xpath(reaction_xpath + "[contains(@class,'meh')]")[0].text

        no_percent_keep = raw_rating_keep.replace('%', '') # remove the '%' char
        no_percent_food = raw_rating_food.replace('%', '')
        no_percent_best = raw_rating_best.replace('%', '')
        no_percent_meh = raw_rating_meh.replace('%', '')

        self.ratings = {
            Rating.KEEP_IT: float(no_percent_keep),
            Rating.FOOD: float(no_percent_food),
            Rating.THE_BEST: float(no_percent_best),
            Rating.MEH: float(no_percent_meh),
        }

    def __parse_image_links(self, tree):
        """
            This method parses the URLs of the images of a monster for
            both sleepy and awakened from a tree
        """
        img_base = '//*[contains(@class, "image-container")]'
        sleepy_xpath = '//img[contains(@class, "wp-post-image")]/@data-lazy-src'
        awake_xpath = '//img[contains(@class, "featured2")]/@src'

        self.links[LinkType.IMAGE_SLEEPY] = tree.xpath(img_base + sleepy_xpath)[0]

        awake_image = tree.xpath(img_base + awake_xpath)
        awake_image_exists = len(awake_image) > 0

        if awake_image_exists:
            self.links[LinkType.IMAGE_AWAKE] = awake_image[0]

    def __parse_alt_links(self, tree):
        """
            This method parses the URL of the fire version of a monster
            from a tree
        """
        elem_xpath = '//*[@id="content-anchor-inner"]//p'
        for anchor in tree.xpath(elem_xpath + '//a'):
            info_obj = self.__parse_alt_link_info(anchor)
            self.links[info_obj['link_type']] = info_obj['alt_link']
