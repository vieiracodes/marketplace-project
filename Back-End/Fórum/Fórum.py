import json

class Forum_thread():
    def __init__(self):
        self.num_thread = 0 #verificar a necessidade depois
        # self.post_json = None #verificar a necessidade depois
        self.thread_topics = None #verificar a necessidade depois(de ser global)
        self.num_comments = None #verificar a necessidade depois

    # Método da classe, para criar um novo tópico
    def Criar_thread(self, user, titulo, comment):
        with open('Back-End/static/json/forum.json', 'r+') as post_data:
            try:
                post_json = json.load(post_data)
                self.num_thread = len(post_json['Threads'])+1

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

            # Fazer um sistema de exceções mais específicas posteriormente
            except:
                print('erro')


    # Método da classe, para adicionar um novo comentário.
    def Comentar(self, user, comment, num_thread):

        with open('Back-End/static/json/forum.json', 'r+') as post_data:
            try:
                post_json = json.load(post_data)
                self.num_comments = len(post_json["Threads"][num_thread]["Thread_comments"])+1

            # Fazer um sistema de exceções mais específicas posteriormente.
            except:
                print('erro')

            post_json["Threads"][num_thread]["Thread_comments"][self.num_comments] = {}
            post_json["Threads"][num_thread]["Thread_comments"][self.num_comments]["Thread_user"] = user
            post_json["Threads"][num_thread]["Thread_comments"][self.num_comments]["Thread.description"] = comment


            with open('Back-End/static/json/forum.json', 'w') as post_save:
                json.dump(post_json, post_save, indent = 3)

    # Método da classe, para recuperar o json das threads
    # (para consultas pelo back-end).
    def Get_threads(self):
        with open('Back-End/static/json/forum.json', 'r+') as post_data:
            self.thread_topics = json.load(post_data)['Threads']
        return self.thread_topics

    # Método da classe, para Editar algum dado do tópico.
    # Mais usado para alterar o status do tópico entre aberto e fechado.
    def Editar_dado(self, num_thread, dado, novo_dado):
        with open('Back-End/static/json/forum.json', 'r+') as post_data:
            try:
                post_json = json.load(post_data)
            # Fazer um sistema de exceções mais específicas posteriormente
            except:
                print('erro')

            post_json["Threads"][num_thread]["Thread_OP"][dado] = novo_dado

            with open('Back-End/static/json/forum.json', 'w') as post_save:
                json.dump(post_json, post_save, indent = 3)

    # Método da classe, para excluir um tópico
    def Excluir_thread(self, num_thread):
        # Excluir a thread mantém as outras threads com o número/id antigo. O
        # número da thread excluida permanece inutilizado, e não será substituido
        # por uma nova thread.
        with open('Back-End/static/json/forum.json', 'r+') as post_data:
            threads_dict = json.load(post_data)
            del threads_dict['Threads'][num_thread]
            print(threads_dict['Threads'])

            with open('Back-End/static/json/forum.json', 'w') as post_save:
                json.dump(threads_dict, post_save, indent = 3)

    #Método da classe, para excluir um comentário
    def Excluir_comment(self, num_thread, num_post):
        with open('Back-End/static/json/forum.json', 'r+') as post_data:
            threads_dict = json.load(post_data)

            print(threads_dict['Threads'][num_thread]["Thread_comments"])
            del threads_dict['Threads'][num_thread]["Thread_comments"][num_post]
            print(threads_dict['Threads'][num_thread]["Thread_comments"])

            with open('Back-End/static/json/forum.json', 'w') as post_save:
                json.dump(threads_dict, post_save, indent = 3)
