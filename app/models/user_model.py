from idna import intranges_contain
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__='mdl_user'
    id: int = Field(primary_key=True)
    auth: str = Field(max_length=20)
    confirmed: int
    policyagreed: int
    deleted: int
    suspended: int
    mnethostid: int
    username: str = Field(max_length=100)
    password: str = Field(max_length=255)
    idnumber: str = Field(max_length=255)
    firstname: str = Field(max_length=100)
    lastname: str = Field(max_length=100)
    email: str = Field(max_length=100)
    emailstop: int
    phone1: str = Field(max_length=20)
    phone2: str = Field(max_length=20)
    institution: str = Field(max_length=255)
    department: str = Field(max_length=255)
    address: str = Field(max_length=255)
    city: str = Field(max_length=120)
    country: str = Field(max_length=2)
    lang: str = Field(max_length=30, default="en")
    calendartype: str = Field(max_length=30, default="gregorian")
    theme: str = Field(max_length=50)
    timezone: str = Field(max_length=100, default="99")
    firstaccess: int
    lastaccess: int
    lastlogin: int
    currentlogin: int
    lastip: str = Field(max_length=45)
    secret: str = Field(max_length=15)
    picture: int
    description: str = Field(nullable=True)
    descriptionformat: int = Field(default=1)
    mailformat: int = Field(default=1)
    maildigest: int = Field(default=0)
    maildisplay: int = Field(default=2)
    autosubscribe: int = Field(default=1)
    trackforums: int
    timecreated: int
    timemodified: int
    trustbitmask: int
    imagealt: str = Field(nullable=True, max_length=255)
    lastnamephonetic: str = Field(nullable=True, max_length=255)
    firstnamephonetic: str = Field(nullable=True, max_length=255)
    middlename: str = Field(nullable=True, max_length=255)
    alternatename: str = Field(nullable=True, max_length=255)
    moodlenetprofile: str = Field(nullable=True, max_length=255)



class Course(SQLModel, table=True):
    __tablename__ = 'mdl_course'
    id: int = Field(primary_key=True, description="The unique identifier for the course.")
    category: int = Field(description="The ID of the category associated with the course.")
    sortorder: int = Field(description="The sort order of the course.")
    fullname: str = Field(description="The full name of the course.")
    shortname: str = Field(description="The short name of the course.")
    idnumber: str = Field(description="An identification number associated with the course.")
    summary: str = Field(description="The summary or description of the course.")
    summaryformat: int = Field(description="The format of the course summary.")
    format: str = Field(description="The format of the course.")
    showgrades: int = Field(description="Indicates whether grades are shown for the course.")
    newsitems: int = Field(description="The number of news items displayed for the course.")
    startdate: int = Field(description="The start date of the course.")
    enddate: int = Field(description="The end date of the course.")
    relativedatesmode: int = Field(description="The mode of relative dates.")
    marker: int = Field(description="The marker associated with the course.")
    maxbytes: int = Field(description="The maximum file size allowed for the course.")
    legacyfiles: int = Field(description="Indicates whether legacy files are enabled for the course.")
    showreports: int = Field(description="Indicates whether reports are shown for the course.")
    visible: int = Field(description="Indicates whether the course is visible.")
    visibleold: int = Field(description="Indicates whether the course is visible to old users.")
    downloadcontent: int|None = Field(default=None, description="Indicates whether content can be downloaded.")
    groupmode: int = Field(description="The group mode of the course.")
    groupmodeforce: int = Field(description="Indicates whether the group mode is forced.")
    defaultgroupingid: int = Field(description="The default grouping ID for the course.")
    lang: str = Field(description="The preferred language of the course.")
    calendartype: str = Field(description="The calendar type preferred by the course.")
    theme: str = Field(description="The theme of the course.")
    timecreated: int = Field(description="The timestamp when the course was created.")
    timemodified: int = Field(description="The timestamp when the course was last modified.")
    requested: int = Field(description="Indicates whether the course was requested.")
    enablecompletion: int = Field(description="Indicates whether completion is enabled for the course.")
    completionnotify: int = Field(description="Indicates whether completion notifications are enabled for the course.")
    cacherev: int = Field(description="The cache revision of the course.")
    originalcourseid: int|None = Field(description="The original course ID.")
    showactivitydates: int|None = Field(description="Indicates whether activity dates are shown for the course.")
    showcompletionconditions: int|None = Field(description="Indicates whether completion conditions are shown for the course.")
    pdfexportfont: str|None = Field(description="The font used for PDF export.")



class UserEnrolment(SQLModel, table=True):
    __tablename__ = 'mdl_user_enrolments'
    id: int = Field(primary_key=True, description="The unique identifier for the user enrolment.")
    status: int = Field(description="The status of the user enrolment.")
    enrolid: int = Field(description="The enrolment ID associated with the user enrolment.")
    userid: int = Field(description="The user ID associated with the user enrolment.")
    timestart: int = Field(description="The start time of the user enrolment.")
    timeend: int = Field(description="The end time of the user enrolment.")
    modifierid: int = Field(description="The ID of the modifier associated with the user enrolment.")
    timecreated: int = Field(description="The timestamp of when the user enrolment was created.")
    timemodified: int = Field(description="The timestamp of when the user enrolment was last modified.")



class Enrol(SQLModel, table=True):
    __tablename__ = 'mdl_enrol'
    id: int = Field(primary_key=True, description="The unique identifier for the enrolment.")
    enrol: str = Field(description="The type of enrolment plugin used.")
    status: int = Field(description="The status of the enrolment.")
    courseid: int = Field(description="The ID of the course associated with the enrolment.")
    sortorder: int = Field(description="The sort order of the enrolment.")
    name: str|None = Field(default=None, description="The name of the enrolment.")
    enrolperiod: int|None = Field(default=0, description="The enrolment period.")
    enrolstartdate: int|None = Field(default=0, description="The start date of the enrolment.")
    enrolenddate: int|None = Field(default=0, description="The end date of the enrolment.")
    expirynotify: int|None = Field(default=0, description="Indicates whether expiry notifications are enabled.")
    expirythreshold: int|None = Field(default=0, description="The expiry threshold.")
    notifyall: int|None = Field(default=0, description="Indicates whether notifications are sent to all users.")
    password: str|None = Field(default=None, description="The password required for enrolment.")
    cost: str|None = Field(default=None, description="The cost associated with enrolment.")
    currency: str|None = Field(default=None, description="The currency used for enrolment.")
    roleid: int|None = Field(default=0, description="The role ID associated with enrolment.")
    customint1: int|None = Field(default=None, description="Custom integer field 1.")
    customint2: int|None = Field(default=None, description="Custom integer field 2.")
    customint3: int|None = Field(default=None, description="Custom integer field 3.")
    customint4: int|None = Field(default=None, description="Custom integer field 4.")
    customint5: int|None = Field(default=None, description="Custom integer field 5.")
    customint6: int|None = Field(default=None, description="Custom integer field 6.")
    customint7: int|None = Field(default=None, description="Custom integer field 7.")
    customint8: int|None = Field(default=None, description="Custom integer field 8.")
    customchar1: str|None = Field(default=None, description="Custom character field 1.")
    customchar2: str|None = Field(default=None, description="Custom character field 2.")
    customchar3: str |None= Field(default=None, description="Custom character field 3.")
    customdec1: float|None = Field(default=None, description="Custom decimal field 1.")
    customdec2: float|None = Field(default=None, description="Custom decimal field 2.")
    customtext1: str|None = Field(default=None, description="Custom text field 1.")
    customtext2: str|None = Field(default=None, description="Custom text field 2.")
    customtext3: str|None = Field(default=None, description="Custom text field 3.")
    customtext4: str|None = Field(default=None, description="Custom text field 4.")
    timecreated: int|None = Field(description="The timestamp when the enrolment was created.")
    timemodified: int|None = Field(description="The timestamp when the enrolment was last modified.")


class Assignment(SQLModel, table=True):
    __tablename__='mdl_assign'
    id: int = Field(primary_key=True, description="The unique identifier for the assignment.")
    course: int = Field(description="The ID of the course associated with the assignment.")
    name: str = Field(description="The name of the assignment.")
    intro: str = Field(description="The introduction or description of the assignment.")
    introformat: int = Field(description="The format of the introduction text.")
    alwaysshowdescription: int = Field(description="Indicates whether the description should always be shown.")
    nosubmissions: int = Field(description="Indicates whether submissions are allowed.")
    submissiondrafts: int = Field(description="Indicates whether submission drafts are allowed.")
    sendnotifications: int = Field(description="Indicates whether notifications are sent.")
    sendlatenotifications: int = Field(description="Indicates whether late notifications are sent.")
    duedate: int = Field(description="The due date of the assignment.")
    allowsubmissionsfromdate: int = Field(description="The date from which submissions are allowed.")
    grade: int = Field(description="The grade associated with the assignment.")
    timemodified: int = Field(description="The timestamp of when the assignment was last modified.")
    requiresubmissionstatement: int = Field(description="Indicates whether a submission statement is required.")
    completionsubmit: int = Field(description="Indicates whether submission is required for completion.")
    cutoffdate: int = Field(description="The cutoff date for the assignment.")
    gradingduedate: int = Field(description="The grading due date for the assignment.")
    teamsubmission: int = Field(description="Indicates whether team submission is allowed.")
    requireallteammemberssubmit: int = Field(description="Indicates whether all team members are required to submit.")
    teamsubmissiongroupingid: int = Field(description="The grouping ID for team submission.")
    blindmarking: int = Field(description="Indicates whether blind marking is enabled.")
    hidegrader: int = Field(description="Indicates whether the grader is hidden.")
    revealidentities: int = Field(description="Indicates whether identities are revealed.")
    attemptreopenmethod: str = Field(description="The method used to reopen attempts.")
    maxattempts: int = Field(description="The maximum number of attempts allowed.")
    markingworkflow: str = Field(description="The marking workflow used.")
    markingallocation: str = Field(description="The marking allocation used.")
    sendstudentnotifications: int = Field(description="Indicates whether student notifications are sent.")
    preventsubmissionnotingroup: int = Field(description="Indicates whether submissions are prevented if not in a group.")
    activity: str| None = Field(description="The activity associated with the assignment.", default=None)
    activityformat: int = Field(description="The format of the activity.")
    timelimit: int = Field(description="The time limit for the assignment.")
    submissionattachments: str = Field(description="The submission attachments allowed for the assignment.")

class Quiz(SQLModel, table=True):
    __tablename__='mdl_quiz'
    id: int = Field(primary_key=True, description="The unique identifier for the quiz.")
    course: int = Field(description="The ID of the course associated with the quiz.")
    name: str = Field(description="The name of the quiz.")
    intro: str = Field(description="The introduction or description of the quiz.")
    introformat: int = Field(description="The format of the introduction text.")
    timeopen: int = Field(description="The timestamp when the quiz opens.")
    timeclose: int = Field(description="The timestamp when the quiz closes.")
    timelimit: int = Field(description="The time limit for completing the quiz.")
    overduehandling: str = Field(description="The handling of overdue submissions.")
    graceperiod: int = Field(description="The grace period for late submissions.")
    preferredbehaviour: str = Field(description="The preferred behavior for the quiz.")
    canredoquestions: int = Field(description="Indicates whether questions can be redone.")
    attempts: int = Field(description="The number of attempts allowed for the quiz.")
    attemptonlast: int = Field(description="Indicates whether the attempt is on the last question.")
    grademethod: str = Field(description="The grading method used for the quiz.")
    decimalpoints: int = Field(description="The number of decimal points used in grading.")
    questiondecimalpoints: int = Field(description="The number of decimal points used for questions.")
    reviewattempt: int = Field(description="Indicates whether review of attempts is enabled.")
    reviewcorrectness: int = Field(description="Indicates whether review of correctness is enabled.")
    reviewmaxmarks: int = Field(description="The maximum marks allowed for review.")
    reviewmarks: int = Field(description="The marks obtained during review.")
    reviewspecificfeedback: int = Field(description="Indicates whether specific feedback is provided during review.")
    reviewgeneralfeedback: int = Field(description="Indicates whether general feedback is provided during review.")
    reviewrightanswer: int = Field(description="Indicates whether the correct answers are revealed during review.")
    reviewoverallfeedback: int = Field(description="Indicates whether overall feedback is provided during review.")
    questionsperpage: int = Field(description="The number of questions displayed per page.")
    navmethod: str = Field(description="The navigation method used in thequiz.")
    shuffleanswers: int = Field(description="Indicates whether answers are shuffled.")
    sumgrades: float = Field(description="The sum of grades for the quiz.")
    grade: float = Field(description="The grade obtained for the quiz.")
    timecreated: int = Field(description="The timestamp when the quiz was created.")
    timemodified: int = Field(description="The timestamp when the quiz was last modified.")
    password: str = Field(description="The password required to access the quiz.")
    subnet: str = Field(description="The subnet allowed to access the quiz.")
    browsersecurity: str = Field(description="The browser security settings for the quiz.")
    delay1: int = Field(description="The delay before starting the quiz.")
    delay2: int = Field(description="The delay before submitting the quiz.")
    showuserpicture: int = Field(description="Indicates whether user pictures are shown.")
    showblocks: int = Field(description="Indicates whether blocks are shown.")
    completionattemptsexhausted: int = Field(description="Indicates whether completion attempts are exhausted.")
    completionminattempts: int = Field(description="The minimum number of attempts required for completion.")
    allowofflineattempts: int = Field(description="Indicates whether offline attempts are allowed.")



class Notification(SQLModel, table=True):
    __tablename__ = 'mdl_notifications'
    id: int = Field(primary_key=True, description="The unique identifier for the notification.")
    useridfrom: int = Field(description="The ID of the user who sent the notification.")
    useridto: int = Field(description="The ID of the user who received the notification.")
    subject: str = Field(description="The subject of the notification.")
    fullmessage: str = Field(description="The full content of the notification.")
    fullmessageformat: int = Field(description="The format of the full message.")
    fullmessagehtml: str = Field(description="The HTML-formatted full message.")
    smallmessage: str = Field(description="A small version of the message.")
    component: str = Field(description="The component associated with the notification.")
    eventtype: str = Field(description="The type of event associated with the notification.")
    contexturl: str = Field(description="The URL associated with the notification context.")
    contexturlname: str = Field(description="The name of the URL associated with the notification context.")
    timeread: int = Field(description="The timestamp when the notification was read.")
    timecreated: int = Field(description="The timestamp when the notification was created.")
    customdata: str = Field(description="Custom data associated with the notification.")

from sqlalchemy import Column, BigInteger, Integer, String, Text, SmallInteger

class Page(SQLModel, table=True):
    __tablename__ = "mdl_page"
    id: int = Field(primary_key=True)
    course: int
    name: str  = Field(sa_column=Column(String(255, collation="C.UTF-8"), nullable=True, default=""))
    intro: str  = Field(sa_column=Column(String(255, collation="C.UTF-8"), nullable=True, default=""))
    introformat: int
    content: str | None = Field(sa_column=Column(String(255, collation="C.UTF-8"), nullable=True, default=""))
    contentformat: int
    legacyfiles: int
    legacyfileslast: int| None = None
    display: int | None = None
    displayoptions: str | None = Field(sa_column=Column(String(255, collation="C.UTF-8"), nullable=True, default=""))
    revision: int  | None = None
    timemodified: int | None = None


class Label(SQLModel, table=True):
    __tablename__ = "mdl_label"
    id: int = Field(primary_key=True)
    course: int
    name: str | None = None
    intro: str | None = None
    introformat: int| None = None
    timemodified: int | None = None
    
