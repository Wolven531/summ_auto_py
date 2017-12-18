"""
    This is the MonsterPage module
"""

import json
import os
from Rating import Rating
from MonsterType import MonsterType
from LinkType import LinkType

class MonsterPage():
    """
        This class represents the parsed result of a single monster
        page
    """

    OVERVIEW_XPATH = '//*[@id="overview-anchor"]/div[2]/div[2]'
    DEFAULT_ELEMENT = MonsterType.FIRE

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
    def parse_alt_link_info(tree, target_xpath):
        """
            This method parses the URL and type of a particular element link
            on a monster page using xpath on a tree
        """
        elem_xpath = '//*[@id="content-anchor-inner"]//p'

        href = tree.xpath(elem_xpath + target_xpath + '/@href')
        href_exists = len(href) > 0

        alt_type = MonsterPage.DEFAULT_ELEMENT

        if href_exists:
            href = href[0]
            href_type = tree.xpath(elem_xpath + target_xpath + '/@title')[0]
            href_type = href_type[0 : href_type.find(' ')].upper()

            if MonsterType.has_value(href_type):
                alt_type = MonsterType[href_type]
        else:
            href = ''

        return {
            'alt_link': href,
            'link_type': MonsterPage.convert_element_to_link_type(alt_type)
        }


    def __init__(self, tree):
        self.links = LinkType.generate_link_dict()
        self.parse_name(tree)
        self.parse_element(tree)
        self.parse_grade(tree)
        self.parse_type(tree)
        self.parse_get_from(tree)
        self.parse_when_awakened(tree)
        self.parse_good_for(tree)
        self.parse_skillup_info(tree)
        self.parse_alt_links(tree)
        self.parse_scores(tree)
        self.parse_ratings(tree)
        self.parse_image_links(tree)
        self.print_mon_info()

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

        return f'{cwd}/data/{lowered}.json'

    def serialize(self, filepath=''):
        """
            This method will attempt to write this instance of MonsterPage
            to a file, determined by the filepath param which defaults to
            using MonsterPage.get_filepath()
        """
        if filepath == '':
            filepath = self.get_filepath()

        serialized_links = []
        serialized_ratings = []

        for link_key in self.links:
            serialized_links.append(
                {link_key.value: self.links[link_key]}
            )

        for rating_key in self.ratings:
            serialized_ratings.append(
                {rating_key.value: self.ratings[rating_key]}
            )

        data = {
            'element': self.element.value,
            'get_from': self.get_from,
            'good_for': self.good_for,
            'grade': self.grade,
            'grade_num': self.grade_num,
            'links': serialized_links,
            'mon_type': self.mon_type,
            'name_awaken': self.awaken_name,
            'name_full': self.full_name,
            'name_sleepy': self.sleepy_name,
            'ratings': serialized_ratings,
            'score_total': self.score_total,
            'score_user': self.score_user,
            'skillup_info': self.skillup_info,
            'when_awaken': self.when_awakened
        }

        with open(filepath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=2)

    def parse_element(self, tree):
        """
            This method parses the element of the monster from a tree
        """
        raw_mon_name = tree.xpath('//h1[@class="main-title"]')[0].text
        raw_mon_name = raw_mon_name.strip()
        first_space_ind = raw_mon_name.find(' ')
        potential_element = raw_mon_name[0 : first_space_ind].upper()

        self.element = MonsterPage.DEFAULT_ELEMENT

        if MonsterType.has_value(potential_element):
            self.element = MonsterType[potential_element]
        else:
            print(f'Error parsing element, got: "{potential_element}"')

    def parse_name(self, tree):
        """
            This method parses a name (and sleepy and awakened) from a tree
        """
        raw_mon_name = tree.xpath('//h1[@class="main-title"]')[0].text
        raw_mon_name = raw_mon_name.strip()
        self.full_name = raw_mon_name
        first_space_ind = raw_mon_name.find(' ')
        paren_ind = self.full_name.find('(')
        self.sleepy_name = self.full_name[first_space_ind + 1 : paren_ind - 1] # -1 for the space
        self.awaken_name = self.full_name[paren_ind + 1 : -1]

    def parse_grade(self, tree):
        """
            This method parses a grade and grade_num from a tree
        """
        xpath_selector = MonsterPage.OVERVIEW_XPATH + '/div[1]/span[2]/p'
        raw_grade = tree.xpath(xpath_selector)[0].text
        self.grade = raw_grade
        self.grade_num = len(self.grade)

    def parse_type(self, tree):
        """
            This method parses the type of a monster from a tree
        """
        xpath_selector = self.OVERVIEW_XPATH + '/div[2]/span[2]/p'
        raw_type = tree.xpath(xpath_selector)[0].text
        self.mon_type = raw_type

    def parse_get_from(self, tree):
        """
            This method parses the get from of a monster from a tree
        """
        xpath_selector = self.OVERVIEW_XPATH + '/div[3]/span[2]/p'
        raw_get_from = tree.xpath(xpath_selector)[0].text
        self.get_from = raw_get_from

    def parse_when_awakened(self, tree):
        """
            This method parses the when awakened of a monster from a tree
        """
        xpath_selector = self.OVERVIEW_XPATH + '/div[4]/span[2]/p'
        raw_when_awakened = tree.xpath(xpath_selector)[0].text
        self.when_awakened = raw_when_awakened

    def parse_good_for(self, tree):
        """
            This method parses the good for of a monster from a tree
        """
        xpath_selector = self.OVERVIEW_XPATH + '/div[5]/span[2]/p'
        raw_good_for = tree.xpath(xpath_selector)[0].text
        self.good_for = raw_good_for

    def parse_skillup_info(self, tree):
        """
            This method parses the skillup info of a monster from a tree
        """
        xpath_selector = self.OVERVIEW_XPATH + '/div[6]/span[2]/p'
        raw_skillup_info = tree.xpath(xpath_selector)[0].text
        self.skillup_info = raw_skillup_info

    def parse_scores(self, tree):
        """
            This method parses a total and user score from a tree
        """
        xpath_rating = '//*[@id="rating-anchor"]'
        xpath_editor = '//*[contains(@class, "editor_rating")]'
        xpath_user = '//*[contains(@class, "user_rating")]'

        raw_score_total = tree.xpath(
            xpath_rating + xpath_editor + '/*[contains(@class, "number")]')[0].text
        raw_score_user = tree.xpath(
            xpath_rating + xpath_user + '/*[contains(@class, "number")]')[0].text

        self.score_total = float(raw_score_total.strip())
        self.score_user = float(raw_score_user.strip())

    def parse_ratings(self, tree):
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

    def parse_image_links(self, tree):
        """
            This method parses the URLs of the images of a monster for
            both sleepy and awakened from a tree
        """
        img_base = '//*[contains(@class, "image-container")]'
        sleepy_xpath = '//img[contains(@class, "wp-post-image")]/@data-lazy-src'
        awake_xpath = '//img[contains(@class, "featured2")]/@src'

        self.links[LinkType.IMAGE_SLEEPY] = tree.xpath(img_base + sleepy_xpath)[0]
        self.links[LinkType.IMAGE_AWAKE] = tree.xpath(img_base + awake_xpath)[0]

    def parse_alt_links(self, tree):
        """
            This method parses the URL of the fire version of a monster
            from a tree
        """
        hrefs_infos = [
            self.parse_alt_link_info(tree, '//a[1]'),
            self.parse_alt_link_info(tree, '//a[2]'),
            self.parse_alt_link_info(tree, '//a[3]'),
            self.parse_alt_link_info(tree, '//a[4]'),
            self.parse_alt_link_info(tree, '//a[5]')
        ]

        for info_obj in hrefs_infos:
            self.links[info_obj['link_type']] = info_obj['alt_link']
