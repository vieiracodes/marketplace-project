import json

class Forum_thread():
    def __init__(self):
        self.num_thread = 0 #verificar a necessidade depois
        self.post_json = None #verificar a necessidade depois
        self.thread_topics = None #verificar a necessidade depois(de ser global)
        self.num_comments = None #verificar a necessidade depois


    def Criar_thread(self, user, titulo, comment):
        with open('Back-End/static/json/forum.json', 'r+') as post_data:
            try:
                post_json = json.load(post_data)

                self.num_thread = len(post_json['Threads'])+1


            # Fazer um sistema de exceções mais específicas posteriormente
            except:
                print('erro')

            post_json["Threads"][self.num_thread] = {}
            post_json["Threads"][self.num_thread]["Thread_OP"] = {}
            post_json["Threads"][self.num_thread]["Thread_OP"]["Thread.OP_user"] = user
            post_json["Threads"][self.num_thread]["Thread_OP"]["Thread.title"] = titulo
            post_json["Threads"][self.num_thread]["Thread_OP"]["Thread.description"] = comment
            post_json["Threads"][self.num_thread]["Thread_OP"]["Thread.status"] = 'Aberto'

            #Abertura dos comentários da thread
            post_json["Threads"][self.num_thread]["Thread_comments"] = {}



            with open('Back-End/static/json/forum.json', 'w') as post_save:
                json.dump(post_json, post_save, indent = 3)



    def Comentar(self, user, comment, num_thread):

        with open('Back-End/static/json/forum.json', 'r+') as post_data:
            try:
                post_json = json.load(post_data)
                self.num_comments = len(post_json["Threads"][num_thread]["Thread_comments"])+1

            # Fazer um sistema de exceções mais específicas posteriormente
            except:
                print('erro')

            post_json["Threads"][num_thread]["Thread_comments"][self.num_comments] = {}
            post_json["Threads"][num_thread]["Thread_comments"][self.num_comments]["Thread_user"] = user
            post_json["Threads"][num_thread]["Thread_comments"][self.num_comments]["Thread.description"] = comment


            with open('Back-End/static/json/forum.json', 'w') as post_save:
                json.dump(post_json, post_save, indent = 3)


    def Get_threads(self):
        with open('Back-End/static/json/forum.json', 'r+') as post_data:
            self.thread_topics = json.load(post_data)['Threads']
        return self.thread_topics
