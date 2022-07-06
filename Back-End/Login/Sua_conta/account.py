#Classe apenas para gerenciar qual funçõa do banco de dados deve ser executada
#Daria pra colocar esse código direto na função da rota do site, ou no código principal
class Account():

    def __init__(self):
        pass


    def account_config(self, recurso):

        # Switch para ver qual recurso está
        if(recurso == "change_data"):
            func_config_account = 'alterar_user'



        elif(recurso == "delete_user"):
            func_config_account = 'deletar_user'



        elif(recurso == "insert_payment"):
            func_config_account = 'insert_payment_method'
            

        # elif(recurso == ""):
        #     pass
        #
        # elif(recurso == ""):
        #     pass

        else:
            return 'abort(406)'


        return f"getattr(Banco_de_dados, '{func_config_account}')(Banco_de_dados, **config_args)"
