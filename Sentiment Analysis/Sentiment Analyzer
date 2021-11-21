import tkinter as tk
import nltk
from nltk import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
import string


class App:

    def __init__(self, root):

        self.root = root
        self.root.geometry('600x800')
        self.root.title('Sentiment Analyzer')
        self.root.bind('<Escape>', lambda e: self.close(e))
        self.widgets()

    def widgets(self):

        text_f = tk.Frame()
        text_f.pack(fill='x')
        title = tk.Label(text_f, text='Sentiment Analysis',
                         font='Arial 12 italic', width=30, height=1, 
                         relief=tk.GROOVE)
        title.pack(pady=10)
        self.tx = tk.Text(text_f, bg='lightyellow', width=70,
                          height=10, relief='sunken')
        self.tx.pack()
        self.tx.insert('1.0','>>> Enter text:')
        btn1 = tk.Button(text_f, text='Analyze', command=self.sent_analysis)
        btn1.pack(side=tk.TOP)

        analysis_f = tk.Frame()
        analysis_f.pack(fill='x')
        positive = tk.LabelFrame(
            analysis_f, text='Positive Score', relief='sunken')
        positive.pack(pady=20)
        neutral = tk.LabelFrame(
            analysis_f, text='Neutral Score', relief='sunken')
        neutral.pack(pady=20)
        negative = tk.LabelFrame(
            analysis_f, text='Negative Score', relief='sunken')
        negative.pack(pady=20)
        compound = tk.LabelFrame(
            analysis_f, text='Compound Score', relief='sunken')
        compound.pack(pady=20)
        verdict = tk.LabelFrame(analysis_f, text='Result', relief='sunken')
        verdict.pack(pady=20)
        self.name_var1 = tk.StringVar()
        self.output_label1 = tk.Label(
            positive, textvariable=self.name_var1, width=50, height=1)
        self.output_label1.pack()
        self.name_var2 = tk.StringVar()
        self.output_label2 = tk.Label(
            neutral, textvariable=self.name_var2, width=50, height=1)
        self.output_label2.pack()
        self.name_var3 = tk.StringVar()
        self.output_label3 = tk.Label(
            negative, textvariable=self.name_var3, width=50, height=1)
        self.output_label3.pack()
        self.name_var4 = tk.StringVar()
        self.output_label4 = tk.Label(
            compound, textvariable=self.name_var4, width=50, height=1)
        self.output_label4.pack()
        self.name_var5 = tk.StringVar()
        self.output_label5 = tk.Label(
            verdict, textvariable=self.name_var5, font='Arial 12 bold', 
            width=50, height=1)
        self.output_label5.pack()

        clear_f = tk.Frame()
        clear_f.pack(fill='x')
        btn2 = tk.Button(clear_f, text='Clear', command=self.clear)
        btn2.pack()

    def sent_analysis(self):

        self.doc = self.tx.get('1.0', 'end')
        results = SentimentAnalysis(self.doc).analyze()
        self.name_var1.set(results['pos'])
        self.name_var2.set(results['neu'])
        self.name_var3.set(results['neg'])
        self.name_var4.set(results['compound'])
        if results['compound'] >= 0.05:
            self.name_var5.set('Positive')
        elif results['compound'] <= - 0.05:
            self.name_var5.set('Negative')
        else:
            self.name_var5.set('Neutral')

    def clear(self):

        # deleting the content from the entry box
        self.name_var1.set('')
        self.name_var2.set('')
        self.name_var3.set('')
        self.name_var4.set('')
        self.name_var5.set('')
        # whole content of text area  is deleted
        self.tx.delete(1.0, tk.END)

    def close(self, event):
        self.root.destroy()


class SentimentAnalysis:

    stopwords = nltk.corpus.stopwords.words('english')
    wordnet_lemmatizer = WordNetLemmatizer()
    sid = SentimentIntensityAnalyzer()

    def __init__(self, text):
        self.text = text

    def preprocess(self):

        self.text = self.text.lower()
        self.text = "".join(
            [i for i in self.text if i not in string.punctuation])
        tokens = word_tokenize(self.text)
        output = [i for i in tokens if i not in SentimentAnalysis.stopwords]
        lemm_text = [SentimentAnalysis.wordnet_lemmatizer.lemmatize(
            word) for word in output]
        self.text = ' '.join(lemm_text)
        return self.text

    def analyze(self):

        self.results = SentimentAnalysis.sid.polarity_scores(self.text)
        return self.results


root = tk.Tk()
app = App(root)
root.mainloop()
