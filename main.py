from openai import OpenAI
import dotenv
import os
import tkinter as tk
import customtkinter


dotenv.load_dotenv()
client = OpenAI(api_key= os.getenv('OPENAI_API_KEY'))

class RecipeCreator:
    def __init__(self):
        #create assistant
        self.assistant = client.beta.assistants.create(
        name='Recipe creator',
        description='You are a recipe creating assistant. You will be given dishes that you will need to create recipes for. You may be given dietary restrictions that you will need to account for. Assemble the steps in an organized list',
        model='gpt-3.5-turbo'
        )
    def GenerateRecipe(self,prompt):
        #create thread
        self.prompt = prompt
        self.thread = client.beta.threads.create(
        messages=[{
        'role':'user',
        'content': f'Create a recipe for {self.prompt}.'
        }]
        )
        #create run
        self.run = client.beta.threads.runs.create_and_poll(
        assistant_id=self.assistant.id,
        thread_id=self.thread.id
        )
        
    def ProduceFile(self,fname):
        self.fname = fname
        #retrieve message
        message = list(client.beta.threads.messages.list(thread_id=self.thread.id,run_id=self.run.id))
        message_content = message[0].content[0].text.value
        print(self.fname)
        #write message to a textfile
        file = open(self.fname + '.txt', 'w')
        file.write(message_content)
        file.close()



class GUI:
    def __init__(self,assistant):
        #initialize window and size
        self.root =tk.Tk()
        self.root.geometry('500x500')
        self.root.title('Recipe Creator')

        #initialize assistant
        self.assistant = assistant

        #create text labels 
        self.welcomeLabel = tk.Label(self.root,text='Welcome to the recipe creator!',font=("Times", "24", "bold underline"))
        self.welcomeDesc = tk.Label(self.root,text='To use this application, enter a dish you would like to generate a recipe for.\nInclude any dietary restrictions along with your dish.\n Then, press the generate button to create your recipe. \nThe recipe will be created in the same directory as this application!',font=('Times','14'))
        self.txtlbl1 = tk.Label(self.root,text='Dish:',font=('Times','10'))
        self.txtlbl2 = tk.Label(self.root,text='File name:',font=('Times','10'))

        #create text entry
        self.dishEntry = tk.Text(self.root,width=35,height=2)
        self.fnameEntry = tk.Text(self.root, width=25,height =2)

        #create buttons
        self.genBtn = tk.Button(self.root,height=2,width=20,text='GENERATE RECIPE',font=('Times','14'),command=self.CreateRecipe)
        self.clrBtn = tk.Button(self.root,height=2,width=10,text='CLEAR',font=('Times','14'),command=self.ClearText)

        #place widgets
        self.welcomeDesc.place(x=25,y=35)
        self.welcomeLabel.pack()
        self.dishEntry.place(x=25,y=140)
        self.fnameEntry.place(x=300, y=140)
        self.genBtn.place(x=25,y=175)
        self.clrBtn.place(x=355,y=175)
        self.txtlbl1.place(x=25,y=120)
        self.txtlbl2.place(x=300,y=120)

    def run(self):
        self.root.mainloop()
    def ClearText(self):
        self.dishEntry.delete('1.0',tk.END)
        self.fnameEntry.delete('1.0',tk.END)
    def CreateRecipe(self):
        self.dish = self.dishEntry.get('1.0',tk.END)
        self.dishEntry.delete('1.0',tk.END)
        self.fname = self.fnameEntry.get('1.0',tk.END)
        self.fnameEntry.delete('1.0',tk.END)
        self.assistant.GenerateRecipe(self.dish)
        self.assistant.ProduceFile(self.fname)
    
def Main():
    #Create instance of recipe creator class
    RecipeAssistant = RecipeCreator()

    #Create GUI Window
    gui = GUI(RecipeAssistant)
    gui.run()

Main()














