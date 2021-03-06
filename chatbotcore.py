from nltk.chat.util import Chat, reflections
import re
import random
import requests
import ast

# === This is the extension code for the NLTK library ===
#        === You dont have to understand it ===

class ContextChat(Chat):
    def respond(self, str, language):
        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)    # pick a random response

                if callable(resp):
                    resp = resp(match.groups())
                
                resp = self._wildcards(resp, match) # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'

                resp = translate_from_english(resp, language)
                return resp

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos+1:pos+2])
            response = response[:pos] + \
                self._substitute(match.group(num + 1)) + \
                response[pos+2:]
            pos = response.find('%')
        return response

    def converse(self, language, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try: user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                user_input = translate_to_english(user_input, language)
                while user_input[-1] in "!.": user_input = user_input[:-1]
                already_asked = add_to_list(user_input)
                if already_asked == 0:
                    print(translate_from_english("You don't remember? You asked this a little bit ago...", language))
                elif already_asked == 1:
                    print(translate_from_english("You just asked this but...", language))
                already_asked = 2
                print(self.respond(user_input, language))

# === Your code should go here ===

def translate_to_english(words, language):
    payload = {'key': 'trnsl.1.1.20190117T132741Z.eb29b4e0109365dc.2bbd22b38b491ee6da903085ed4e941c6ab051d0', 'text': words, 'lang':language+'-en'}
    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=payload)
    output = ast.literal_eval(r.text)
    output = output.get("text")[0]
    return output

def translate_from_english(words, language):
    payload = {'key': 'trnsl.1.1.20190117T132741Z.eb29b4e0109365dc.2bbd22b38b491ee6da903085ed4e941c6ab051d0', 'text': words, 'lang':'en-'+language}
    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=payload)
    output = ast.literal_eval(r.text)
    output = output.get("text")[0]
    return output

shopping_list = [""]

def add_to_list(item):
    '''
    This function adds an item to the shopping list.
    If given item is already in the list it returns
    False, otherwise it returns True
    '''
    if item == shopping_list[0]:
        return 0
    elif item in shopping_list:
        return 1
    else:
        shopping_list.append(item)
        return 2

pairs = [
    # answer to questions
    [
        r'(where)(.*)(school|asw)(.*)', 
        [lambda matches: 'We are located right on the edge of Warsaw, next to the small town of Konstancin-Jeziorna. Our street adress is Warszawska 202 05-520 Konstancin-Jeziorna, Poland. Here is a link to our school on maps. http://bit.ly/aswmap'],
    ],
    [
        r'(.*)(how)(.*)(much)(.*)(tuition|tuiton|tution)(.*)',
        [lambda matches: 'Tuition varies from grade to grade. The chart can be found here: http://bit.ly/aswadmissionscost'],
    ],
    [
        r'(.*)(when)(.*)(school)(.*)(year)(.*)',
        [lambda matches: "The school year varies from year to year, but starts in late August, and goes through mid June. We do have a three week Christmas break, as well as several week long breaks throughout the year. Is there anything else you'd like to know?"],
    ],
    [
        r'(.*)(how)(.*)(apply)(.*)',
        [lambda matches: 'Please download and follow the step-by- step User Guide to Admissions 2019-2020 for specific information on each step: \n> http://bit.ly/ASWAdmissionsGuide <\nIf you have any questions or queries about the application process, please contact the Admissions team.'],
    ],
        [
        r'(.*)(when)(.*)(apply)(.*)',
        [lambda matches: 'Annual application process: Applications for the 2019-2020 school year can be submitted starting from September 2018. Families applying for mid-year enrolment can also apply one year ahead.\nIf you are interested in enrolling your child in more than 12 months from now, please complete our online inquiry form and we will contact you when applications open: http://bit.ly/ASWinquire\nMost of the spaces are allocated by April but openings may become available in the months after that.'],
    ],
    [
        r'(.*)(bus)(.*)',
        [lambda matches: 'A door-to-door bus service is available for a fee for students living in the wider Warsaw area. At the end of the school day buses depart right after school and again at the end of after-school activities.'],
    ],
    [
        r'(.*)(uniform)(.*)',
        [lambda matches: 'At ASW students do not wear a school uniform but are required to dress appropriately for school. Middle and High School students have a Physical Education uniform. Do you have any other questions for me?'],
    ],
    [
        r'(.*)(placement test)(.*)',
        [lambda matches: 'Students applying for Grades 6-12 whose mother tongue is not English or who have not been using English as their primary academic language, will be asked to complete an English language test. Tests in math and foreign language may also be administered to determine appropriate placement in these courses.'],
    ],
    [
        r'(.*)(medical)(.*)',
        [lambda matches: 'Each newly admitted student must have a medical check-up prior to enrolling. The Physical Examination form must be completed by a qualified, licensed health care provider. The check-up should be done no more than 12 months prior to the student’s start date. It must include proof of a Tuberculosis screening and a copy of the child’s vaccination record. A student is not authorised to start school unless the completed Physical Examination form has been submitted to ASW.'],
    ],
    [
        r'(.*)(boarding)(.*)',
        [lambda matches: 'ASW does not offer boarding. Students enrolled at ASW must reside with their parents or a legal guardian. Is there anything else I can help you with?'],
    ],
    [
        r'(.*)(meals)(.*)',
        [lambda matches: 'Fresh, healthy meals and snacks are offered in our cafeteria for a fee. Students may also bring their own lunch from home. I can help you with any other questions you may have.'],
    ],
    [
        r'(.*)(how)(.*)(long)(.*)(day)(.*)',
        [lambda matches: 'School starts at 8:30 and ends at 15:30. For grades 11 and 12, the school day starts at 8:20 and finishes at 15:20. On Wednesdays, all students start school at 9:30 and end at 15:30. There are a variety of after-school activities at the end of the school day.'],
    ],
    [
        r'(.*)(after school|extra|activities)(.*)',
        [lambda matches: 'In order to see the list of after school activities visit the school website: https://www.aswarsaw.org/learning/athletics'],
    ],
    [
        r'(.*)(accept)(.*)(special)(.*)(needs)(.*)',
        [lambda matches: 'ASW welcomes students with a wide range of abilities and interests. Each division, Elementary, Middle and High School, has a Learning Support Program. The program is designed to provide assistance to struggling learners and students who have an identified mild to moderate learning disability or learning difference that requires educational support. ASW currently does not have the personnel capacity to support children with intense learning disabilities. Students with significant social-emotional difficulties who need a special learning environment may not be eligible for admission.'],
    ],
    [
        r'(.*)(application)(.*)(fee)(.*)(refundable|refund)(.*)',
        [lambda matches: 'In short, no. The application fee is a non-refundable administrative fee, charged to cover the costs of processing your child’s application, including testing and interviewing if required.'],
    ],
    [
        r'(.*)(different)(year)(.*)(transition)(.*)',
        [lambda matches: 'Each student’s record is considered carefully. Normally, students who have just completed a grade level (American system equivalent) in their home country will not be promoted to the next grade level mid-year at ASW as this would mean skipping months or even a full semester of that year’s work and leading to gaps in learning. Additionally, students who in future years return to an alternative calendar are often significantly impacted even more. Review of a student’s full record, relevant assessments, and other pertinent information may be used in making an alternative placement, if the body of evidence supports that decision after being reviewed by school administration.'],
    ],
        [
        r'(.*)(withdrawal)(.*)',
        [lambda matches: 'In order to withrdraw your child from the school send an e-mail to the admission’s office at admissions@aswarsaw.org notifying the name of the student(s) who is withdrawing, the last day of attendance, and the reason for withdrawal.']
    ],
    [
        r'(.*)(offer|do|give)(.*)(scholarship|scholarships)(.*)',
        [lambda matches: 'Unfortunately, we do not offer any scholarships at the American School of Warsaw.'],
    ],
     [
        r'(.*)(space|availability|room)(.*)(students|kid|child|son|daughter|bieng)(.*)',
        [lambda matches: 'Admission will be decided based on space availability and in line with the priority rules of the ASW admissions policy. You may view the admissions policy at https://www.aswarsaw.org/admissions/admissions-policy.'],
    ],
    [
        r'(.*)(offer|have|do)(.*)(IB)(.*)',
        [lambda matches: 'The IB Diploma Program at ASW welcomes all students in grades 11 and 12 to participate, either as a full IB Diploma student or taking part in individual Courses. The rewards of participation are high and we hope to see all of our students benefiting from such a well-regarded educational model.'],
    ],
    [
        r'(.*)(full)(.*)(IB)(.*)',
        [lambda matches: 'Although we encourage all students to consider the full IB Diploma and will support all students who wishes to pursue it, we recognize that the IBDP may not fit every student in all situations. All students at ASW graduate with a fully accredited high school diploma, giving them access to postsecondary schools worldwide. In addition, students may elect to take IBDP Courses, which may provide them certain advantages in university applications, college credit, or a combination thereof. Please speak with the IBDP Coordinator or the High School Counselors for guidance and further information.'],
    ],
    [
        r'(.*)(how)(.*)(contact)(.*)(admissions|people)(.*)', 
        [lambda matches: 'In order to contact the good people at the admissions office please email admissions@aswarsaw.org or call +48 22 702 8500.'],
    ],
    [
        r'(.*)(need|required|require|needed)(.*)(apply)(.*)', 
        [lambda matches: 'An application to the American School of Warsaw will be complete when we receive: Student’s Birth Certificate Copy, Student’s Passport Copy, Both Parent’s Passport Copies, 2 Years of School Records or Transcripts, Online Teacher Recommendations, In case of special needs full information and copies of relevant reports must be submitted, Completed Online Application Form, $750 USD Application Fee.'],
    ],
    [
        r'(.*)(visit|tour)(.*)(school|asw)(.*)', 
        [lambda matches: 'We encourage all future potential students and families the opportunity to meet with the ASW admissions team and tour our school and facilities. Middle School and High School tours are held on most Tuesdays, at 11 am while school is in progress. Elementary School tours are help on most Wednesdays, at 10 am while school is in progress. You can register for a tour by emailing the admission’s office at admissions@aswarsaw.org.'],
    ],
    [
        r'(.*)(where|what)(.*)(policies|rules)(.*)', 
        [lambda matches: 'For more information regarding our Upper School policies, please refer to our ASW Upper School Handbook at: https://resources.finalsite.net/images/v1536590120/warsaw/rgdqgo0gelreo7vp041o/ASW_handbook_upper_school_1.pdf.'],
    ],
    [
        r'(.*)(have|does|offer)(.*)(Parent Teacher Orginization|PTO)(.*)', 
        [lambda matches: 'The PTO provides support for ongoing activities of teachers in individual classrooms, grades, and all three of the school divisions that comprise ASW. All parents of students at the school and the ASW faculty make up the general membership of the PTO. For more information please visit the school website.'],
    ],
    [
        r'(.*)(have|does|offer|provide|do)(.*)(learning support)(.*)', 
        [lambda matches: 'The American School of Warsaw strives to set the highest standards of learning for each student at his or her own stage of development, within the context of the ASW curriculum. Understanding that all students learn, grow, and develop in different ways, following ASW’s Learning Support Process, the Learning Support Department provides support services for students who are struggling and students with identified mild to moderate learning needs. The goal is to assist students in reaching their highest potential academically, socially and emotionally.'],
    ],
    [
        r'(.*)(what|how)(.*)(learning support)(.*)', 
        [lambda matches: 'We believe that all students learn best when they are educated with typically developing peers, thus nurturing an atmosphere of tolerance and empathy. Students are initiated into the Learning Support Process by recognition of a difficulty with the Student Study Team (SST). The Student Study Team (SST) consists of learning support teachers, counsellors, subject teachers, the principal and vice-principal. Students are first supported through classroom strategies and consultation with teachers. When students require more support to be successful, they may receive additional aid by one of the professionals in the Learning Support Department. Assistance may be in the form of short term intervention, in-class support, evaluation and/or formal learning support services and classes. The Study Skills Class and the Learning Support Class may take the place of an elective class (grades 6 - 10) or an unsupervised Self-Directed study period (grades 10 - 12).'],
    ],
    [
        r'(.*)(when)(.*)(break)(.*)', 
        [lambda matches: 'You can find out more information including all our important dates on our American School of Warsaw calendar at: https://www.aswarsaw.org/about-us/calendar.'],
    ],

    # conversation stuff
    [
        r'(.*)(hello|hi|greetings|sup|howdy)(.*)', 
        [lambda matches: 'Hello, what can I help you with?'],
    ],
    [
        r'(.*)(what)(.*)(your)(.*)(name)(.*)', 
        [lambda matches: 'I\'m Admissions Bot. It\'s a pleasure to meet you.'],
    ],
    [
        r'(.*)(what)(.*)(you)(.*)(do)(.*)', 
        [lambda matches: 'I am a bot intended to answer your questions about admission. Go ahead, ask me something about admissions.'],
    ],
    [
        r'(.*)(are)(.*)(you)(.*)(alive)(.*)', 
        [lambda matches: 'It depends on what you count as alive.'],
    ],
    [
        r'(.*)(are)(.*)(you)(.*)(real)(.*)', 
        [lambda matches: 'It depends on what you count as real.'],
    ],
    [
        r'(.*)(are)(.*)(you)(.*)(bot|robot)(.*)', 
        [lambda matches: 'Indeed I am, and my purpose is to help you find out more about admissions.'],
    ],
    [
        r'(.*)(find|learn|ask)(.*)(admissions|admission)(.*)', 
        [lambda matches: "That's what I'm here for, feel free to ask me anything about admissions."],
    ],
    [
        r'(.*)(how)(.*)(quit|exit|leave)(.*)', 
        [lambda matches: 'In order to quit simply type: quit.'],
    ],
    

    # quit and error, they must be last
    [
        r'(quit)',
        ["Goodbye."],
    ],
    [
        r'(.*)',
        ["I'm sorry, I'm not sure I understand. Make sure you didn't misspell something."],
    ],
]

if __name__ == "__main__":
    while True:
        print("1) Polski") # polish
        print("2) 한국어") # korean
        print("3) 中文") # chinese
        print("4) Español") # spanish
        print("5) Deutsch") # german
        print("6) Français") # french
        print("7) English") # english
        translate = input("Please choose the number by the language you would like.\n>")
        try:
            translate = int(translate)
        except ValueError:
            translate = input("Please only type a number.\n>")
        else:
            if translate == 1:
                language = "pl"
                break
            elif translate == 2:
                language = "ko"
                break
            elif translate == 3:
                language = "zh"
                break
            elif translate == 4:
                language = "es"
                break
            elif translate == 5:
                language = "de"
                break
            elif translate == 6:
                language = "fr"
                break
            elif translate == 7:
                language = "en"
                break
            else:
                print("{} is not a number you can choose.".format(translate))
    print(translate_from_english("Hi, I'm the ASW Admissions Bot. It's a pleasure to meet you.", language))
    print(translate_from_english("What can I help you with?", language))
    chat = ContextChat(pairs, reflections)
    chat.converse(language)
