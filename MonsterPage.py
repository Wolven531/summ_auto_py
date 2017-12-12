"""
    This is the Monster page module
"""
class MonsterPage():
    """
        This class represents the parsed result of a single monster
        page
    """

    OVERVIEW_XPATH = '//*[@id="overview-anchor"]/div[2]/div[2]'
    SCORE_XPATH = '//*[@id="rating-anchor"]/div[3]/div/div/div[2]/div[1]'
    ELEMENT_ALT_XPATH = '//*[@id="content-anchor-inner"]/p[1]'

    @staticmethod
    def get_next_element(element):
        """
            This method returns the next element in the sequence
            Vinny saw in the code, o_O
        """
        if element == 'Dark':
            return 'Fire'
        if element == 'Fire':
            return 'Water'
        if element == 'Water':
            return 'Wind'
        if element == 'Wind':
            return 'Light'
        return 'Dark'

    @staticmethod
    def parse_alt_link(tree, target_xpath):
        """
            This method parses the URL of a particular element version of a monster
            using xpath on a tree
        """
        href = tree.xpath(target_xpath)
        href_exists = len(href) > 0
        href = href[0] if href_exists else ''
        return href

    def __init__(self, tree):
        self.parse_name(tree)
        self.parse_grade(tree)
        self.parse_type(tree)
        self.parse_get_from(tree)
        self.parse_when_awakened(tree)
        self.parse_good_for(tree)
        self.parse_skillup_info(tree)
        self.parse_alts(tree)
        self.parse_scores(tree)
        self.print_mon_info()

    def print_mon_info(self):
        """
            This method prints out the basic information parsed from a MonsterPage
        """
        print(f'Name: {self.full_name}')
        print(f'Element: {self.element}')
        print(f'Grade: {self.grade}')
        print(f'Type: {self.mon_type}')
        print(f'Get From: {self.get_from}')
        print(f'Awakened: {self.when_awakened}')
        print(f'Good For: {self.good_for}')
        print(f'Skill Up Info: {self.skillup_info}')
        print(f'Total Score: {self.score_total}')
        print(f'User Score: {self.score_user}')

    def parse_name(self, tree):
        """
            This method parses a name (and sleepy and awakened) from a tree
        """
        raw_mon_name = tree.xpath('//h1[@class="main-title"]')[0].text
        self.full_name = raw_mon_name.strip()
        paren_ind = self.full_name.find('(')
        first_space_ind = self.full_name.find(' ')
        self.sleepy_name = self.full_name[0 : paren_ind - 1] # -1 for the space
        self.awaken_name = self.full_name[paren_ind + 1 : -1]
        self.element = self.full_name[0 : first_space_ind]

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
        raw_score_total = tree.xpath(
            MonsterPage.SCORE_XPATH + '/div[2]/div/div[1]/div/div/div/div[2]/div')[0].text
        raw_score_user = tree.xpath(
            MonsterPage.SCORE_XPATH + '/div[3]/div/div[1]/div/div/div/div[2]/div')[0].text
        self.score_total = float(raw_score_total.strip())
        self.score_user = float(raw_score_user.strip())

    def parse_alts(self, tree):
        """
            This method parses the URL of the fire version of a monster
            from a tree
        """
        href1 = self.parse_alt_link(tree, MonsterPage.ELEMENT_ALT_XPATH + '/a[1]/@href')
        href2 = self.parse_alt_link(tree, MonsterPage.ELEMENT_ALT_XPATH + '/a[2]/@href')
        href3 = self.parse_alt_link(tree, MonsterPage.ELEMENT_ALT_XPATH + '/a[3]/@href')
        href4 = self.parse_alt_link(tree, MonsterPage.ELEMENT_ALT_XPATH + '/a[4]/@href')

        if self.element == 'Dark':
            self.link_dark = None
            self.link_fire = href1
            self.link_water = href2
            self.link_wind = href3
            self.link_light = href4
        elif self.element == 'Fire':
            self.link_dark = href4
            self.link_fire = None
            self.link_water = href1
            self.link_wind = href2
            self.link_light = href3
        elif self.element == 'Water':
            self.link_dark = href3
            self.link_fire = href4
            self.link_water = None
            self.link_wind = href1
            self.link_light = href2
        elif self.element == 'Wind':
            self.link_dark = href2
            self.link_fire = href3
            self.link_water = href4
            self.link_wind = None
            self.link_light = href1
        else:
            self.link_dark = href1
            self.link_fire = href2
            self.link_water = href3
            self.link_wind = href4
            self.link_light = None
