from rest_framework import serializers


class UserProfileInsertSerializer(serializers.Serializer):
    FirstName = serializers.CharField(required=True)
    LastName = serializers.CharField(required=True )
    Email = serializers.CharField(required=True )
    Password = serializers.CharField(required=True )
    Phone = serializers.CharField(required=True )
    Address = serializers.CharField(required=False, allow_null=True, allow_blank=True )
    City = serializers.CharField(required=True )
    Country = serializers.CharField(required=True )
    Pincode = serializers.CharField(required=True )
    class Meta:
        fields = '__all__'

class RegisterYourProductFormSerializer(serializers.Serializer):
    UserID = serializers.CharField(required=True)
    ProductID = serializers.CharField(required=True)
    PartNumber = serializers.CharField(required=True )
    SerialNumber = serializers.CharField(required=True )
    PurchasePlatform = serializers.CharField(required=True )
    Distributor = serializers.CharField(required=True )
    class Meta:
        fields = '__all__'
        
        


class GoogleLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'

class EmailOtpLoginSerializer(serializers.Serializer):
    Email = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'

class EmailOtpVerifySerializer(serializers.Serializer):
    Email = serializers.CharField(required=True)
    OTP = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'


class SupportsiteForm_s(serializers.Serializer):
    FirstName = serializers.CharField(required=True)
    LastName = serializers.CharField(required=True)
    Email = serializers.CharField(required=True)
    PhoneNumber = serializers.CharField(required=True)
    Company = serializers.CharField(required=True)
    Message = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'

class MasterProductDetailSerializer(serializers.Serializer):
    ProductID = serializers.CharField(required=True)
    UserID = serializers.CharField(required=False , allow_null = True ,allow_blank=True)
    class Meta:
        fields = '__all__'

class MasterProductFileAccessUrlSerializer(serializers.Serializer):
    FileID = serializers.CharField(required=True)
    ProductID = serializers.CharField(required=True)
    UserID = serializers.CharField(required=False , allow_null = True ,allow_blank=True)
    class Meta:
        fields = '__all__'
        
class SiteFAQDetailByID_s(serializers.Serializer):
    FAQID = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'

class forumsearch_s(serializers.Serializer):
    term = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'
        
class topicsearch_s(serializers.Serializer):
    term = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'

class addreply_s(serializers.Serializer):
    userid = serializers.CharField(required=True)
    topicid = serializers.CharField(required=True)
    reply = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'


class topicdetail_s(serializers.Serializer):
    topicid = serializers.CharField(required=True)
    # prodid = serializers.CharField(required=True)
    userid = serializers.CharField(required=False, allow_null = True, allow_blank = True)
    class Meta:
        fields = '__all__'


class addtopicreply_s(serializers.Serializer):
    userid = serializers.CharField(required=True)
    forumid = serializers.CharField(required=True)
    topic = serializers.CharField(required=True)
    reply = serializers.CharField(required=False, allow_null = True, allow_blank = True)
    class Meta:
        fields = '__all__'


class forumtopics_s(serializers.Serializer):
    forumid = serializers.CharField(required=True)
    userid = serializers.CharField(required=False, allow_null = True, allow_blank = True)
    class Meta:
        fields = '__all__'


class forumcategorylistsearch_s(serializers.Serializer):
    SearchTerm = serializers.CharField(required=False, allow_null = True, allow_blank = True)
    class Meta:
        fields = '__all__'

class opportunityregister_s(serializers.Serializer):
    userid=serializers.CharField(required=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    companyName = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    salesName = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    salesEmail = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    salesPhone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    faeName = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    faeEmail = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    faePhone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    customerCompanyName = serializers.CharField(required=True)
    customerMarket = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    postalcode = serializers.CharField(required=True)
    country = serializers.CharField(required=True)
    customerwebsite = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    engineerName1 = serializers.CharField(required=True)
    engineerEmail1 = serializers.CharField(required=True)
    engineerName2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    engineerEmail2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    engineerName3 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    engineerEmail3 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    projectName = serializers.CharField(required=True)
    projectDesc = serializers.CharField(required=True)
    prototypeDate = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    productionDate = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    projectType = serializers.CharField(required=True)
    eau = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    logicPdModelNumber = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    logicPdModelNumber2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    logicPdModelNumber3 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    comment=serializers.CharField(required=False, allow_null=True, allow_blank=True)
    class Meta:
        fields = '__all__'

class opportunitybyid_s(serializers.Serializer):
    userid = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'



class opportunitylist_s(serializers.Serializer):
    userid = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'




class topicbyid_s(serializers.Serializer):
    topicid = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'



class forumbyid_s(serializers.Serializer):
    forumid = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'




class FeedbackForm_s(serializers.Serializer):
    FirstName = serializers.CharField(required=True)
    LastName = serializers.CharField(required=True)
    Contact = serializers.CharField(required=True)
    Email = serializers.CharField(required=True)
    Company = serializers.CharField(required=True)
    FeedbackType = serializers.CharField(required=True)
    Feedback = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'


class TDGForumSearch_s(serializers.Serializer):
    SearchTerm = serializers.CharField(required=False , allow_null=True , allow_blank=True)
    StartDate = serializers.CharField(required=False , allow_null=True , allow_blank=True)
    EndDate = serializers.CharField(required=False , allow_null=True , allow_blank=True)
    class Meta:
        fields = '__all__'


class opportunityupdate_s(serializers.Serializer):
    userid = serializers.CharField(required=True)
    opportunityid = serializers.CharField(required=True)
    FirstName = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    LastName = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    CompanyName = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    Email = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    Phone = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    SalesName = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    SalesEmail = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    SalesPhone = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    FAEName = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    FAEEmail = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    FAEPhone = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    CustomerCompanyName = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    CustomerMarket = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    Address = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    City = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    State = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    PostalCode = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    Country = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    CustomerWebsite = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    EngineerName1 = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    EngineerEmail1 = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    EngineerName2 = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    EngineerEmail2 = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    EngineerName3 = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    EngineerEmail3 = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    ProjectName = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    ProjectDescription = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    PrototypeDate = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    ProductionDate = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    ProjectType = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    EAU = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    LogicPDModelNumber = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    LogicPDModelNumber2 = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    LogicPDModelNumber3 = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)

    class Meta:
        fields = '__all__'

class TopicReplySearch_s(serializers.Serializer):
    TopicID = serializers.CharField(required=True)
    SearchTerm = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'



class GetUserDetails_s(serializers.Serializer):
    UserId = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'

class GetUserProductDetailsSerilaizer(serializers.Serializer):
    UserId = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'

class UserDetailsUpdateSerilaizer(serializers.Serializer):
    UserId = serializers.CharField(required=True)
    FirstName = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    LastName = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    Mobile=serializers.CharField(required=False,allow_null=True,allow_blank=True)

    class Meta:
        fields = '__all__'
        
class MicrosoftLogin_s(serializers.Serializer):
    AutherizedCode = serializers.CharField(required=True)
    class Meta:
        fields = '__all__'



