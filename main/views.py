from rest_framework import generics




#from permissions import IsAuthenticatedOrCreate
#from rest_framework.authentication import BasicAuthentication
#
#class SignUp(generics.CreateAPIView):
#    '''
#    Signup view for API with oauth 
#    '''
#    queryset = User.objects.all()
#    serializer_class = SignUpSerializer
#    permission_classes = (IsAuthenticatedOrCreate,)

#class Login(generics.ListAPIView):
#    '''
#    Login view for API with oauth
#    '''
#    queryset = User.objects.all()
#    serializer_class = LoginSerializer
    
    #BasicAuthentication needs to change to SessionAuthentication or some other variant
#    authentication_classes = (BasicAuthentication,)

#    def get_queryset(self):
#        return [self.request.user]
