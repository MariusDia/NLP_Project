from re import sub
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from class_architecture import SubmissionCollection
from wordcount import calculateJacquard, pearsonCorrelation
from histograms import separateOverlapSubCommentHists, mixedOverlapSubCommentHists
from LDA import performLDA

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Gui(QMainWindow):
   def __init__(self):
      super().__init__()

      self.setWindowTitle("Project 18: Climate Change News Analysis. Discovering Arguments")

      self.w = QWidget()
      self.w.setWindowTitle("Project 18: Climate Change News Analysis. Discovering Arguments")
      self.w.setStyleSheet("background-color:black;")
      
      self.setCentralWidget(self.w)

      self.screen = QApplication.primaryScreen()
      self.size = self.screen.size()

      self.page_layout = QVBoxLayout(self)
      self.buttonsLayout = QHBoxLayout(self)
      self.menuLayout = QHBoxLayout(self)
      self.errorMsg = QHBoxLayout(self)
      self.contentLayout1 = QVBoxLayout(self)
      self.contentLayout1a = QHBoxLayout(self)
      self.contentLayout2 = QVBoxLayout(self)
      self.contentLayout2a = QHBoxLayout(self)
      self.contentLayout3 = QVBoxLayout(self)
      self.contentLayout3a = QVBoxLayout(self)
      self.contentLayout3b = QVBoxLayout(self)
      self.contentLayout3c = QVBoxLayout(self)
      self.contentLayout4 = QVBoxLayout(self)
      self.contentLayout4a = QVBoxLayout(self)
      self.stretch = QHBoxLayout(self)
      
      self.footer = QLabel(self)
      self.footer.setText("Emy LIEUTAUD - Marius DIAMANT - Giacomo ZAMPROGNO")
      self.footer.setStyleSheet("color:white;")
      self.footer.setFont(QFont("Calibri", 10))
      self.footer.resize(500, 20)
      self.widthFooter = self.footer.fontMetrics().boundingRect(self.footer.text()).width()
      self.footer.move(int(self.size.width()/2 - self.widthFooter/2), int(self.size.height()/1.12))

      self.logo = QLabel()
      self.logoReddit = QPixmap('images/logo_reddit.png')
      self.logoReddit = self.logoReddit.scaledToWidth(int((self.size.width())/28))
      self.logo.setPixmap(self.logoReddit)
      self.logo.setFixedSize(90, 90)
      self.logo.move(int(self.size.width()/80), int(self.size.height()/150))

      self.query = QLabel()
      self.query.setText("Enter keyword(s): ")
      self.query.setStyleSheet("color:white;")
      self.query.setFont(QFont("Calibri", 14))
      self.query.setFixedSize(160, 25)
      self.query.move(int((self.size.width())/18), int((self.size.height())/27))

      self.lineQuery = QLineEdit()
      self.lineQuery.setStyleSheet("color:white;background-color:#3b3b45")
      self.lineQuery.setFont(QFont("Calibri", 14))
      self.lineQuery.setFixedSize(250, 45)
      self.lineQuery.move(int((self.size.width())/7), int((self.size.height())/35))

      self.submissions = QLabel()
      self.submissions.setText("Number of submissions: ")
      self.submissions.setStyleSheet("color:white;")
      self.submissions.setFont(QFont("Calibri", 14))
      self.submissions.setFixedSize(225, 25)
      self.submissions.move(int((self.size.width())/3.35), int((self.size.height())/27))

      self.lineSubmission = QLineEdit()
      self.lineSubmission.setValidator(QIntValidator())
      self.lineSubmission.setStyleSheet("color:white;background-color:#3b3b45")
      self.lineSubmission.setFont(QFont("Calibri", 14))
      self.lineSubmission.setFixedSize(60, 45)
      self.lineSubmission.setMaxLength(3)
      self.lineSubmission.setAlignment(Qt.AlignCenter)
      self.lineSubmission.move(int((self.size.width())/2.39), int((self.size.height())/35))

      self.comments = QLabel()
      self.comments.setText("Number of comments per submissions: ")
      self.comments.setStyleSheet("color:white;")
      self.comments.setFont(QFont("Calibri", 14))
      self.comments.setFixedSize(365, 25)
      self.comments.move(int((self.size.width())/2.12), int((self.size.height())/27))

      self.lineComments = QLineEdit()
      self.lineComments.setValidator(QIntValidator())
      self.lineComments.setStyleSheet("color:white;background-color:#3b3b45")
      self.lineComments.setFont(QFont("Calibri", 14))
      self.lineComments.setFixedSize(55, 45)
      self.lineComments.setMaxLength(3)
      self.lineComments.setAlignment(Qt.AlignCenter)
      self.lineComments.move(int((self.size.width())/1.51), int((self.size.height())/35))

      self.subReddit = QLabel()
      self.subReddit.setText("SubReddit(s): ")
      self.subReddit.setStyleSheet("color:white;")
      self.subReddit.setFont(QFont("Calibri", 14))
      self.subReddit.setFixedSize(125, 25)
      self.subReddit.move(int((self.size.width())/1.395), int((self.size.height())/27))

      self.comboSubReddit = QComboBox()
      self.comboSubReddit.addItems(sorted(['all', 'environment', 'worldnews', 'vegan', 'science', 'collapse', 'europe', 'unpopularopinion']))
      self.comboSubReddit.setStyleSheet("color:white;background-color:#3b3b45")
      self.comboSubReddit.setFont(QFont("Calibri", 14))
      self.comboSubReddit.setFixedSize(210, 45)
      self.comboSubReddit.move(int((self.size.width())/1.27), int((self.size.height())/35))

      self.buttonFont = QFont("Calibri", 15)
      self.buttonFont.setBold(True)

      self.submit = QPushButton("Submit")
      self.submit.setStyleSheet("color:white;background-color:#ff4500;border-radius:4px;")
      self.submit.setFixedSize(110, 45)
      self.submit.setFont(self.buttonFont)
      self.submit.move(int((self.size.width())/1.085), int((self.size.height())/35))
      self.submit.setCursor(Qt.PointingHandCursor)
      self.submit.clicked.connect(self.clicked)

      self.isSubmit = False

      self.progress = QLabel()

      self.error = QLabel(self)
      self.error.setFont(self.buttonFont)

      self.buttonHistoSep = QPushButton("Separated Histograms")
      self.buttonHistoSep.pressed.connect(self.getHistoSep)
      self.buttonHistoSep.setFont(self.buttonFont)
      self.buttonHistoSep.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
      self.buttonHistoSep.resize(110, 45)
      self.buttonHistoSep.setCursor(Qt.PointingHandCursor)

      self.buttonHistoMix = QPushButton("Mixed Histograms")
      self.buttonHistoMix.pressed.connect(self.getHistoMix)
      self.buttonHistoMix.setFont(self.buttonFont)
      self.buttonHistoMix.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
      self.buttonHistoMix.resize(110, 45)
      self.buttonHistoMix.setCursor(Qt.PointingHandCursor)

      self.buttonJaccard = QPushButton("Jaccard indexes")
      self.buttonJaccard.pressed.connect(self.getJaccardIndex)
      self.buttonJaccard.setFont(self.buttonFont)
      self.buttonJaccard.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
      self.buttonJaccard.resize(110, 45)
      self.buttonJaccard.setCursor(Qt.PointingHandCursor)

      self.buttonPearson = QPushButton("Pearson correlations")
      self.buttonPearson.pressed.connect(self.getPearsonCorrelation)
      self.buttonPearson.setFont(self.buttonFont)
      self.buttonPearson.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
      self.buttonPearson.resize(110, 45)
      self.buttonPearson.setCursor(Qt.PointingHandCursor)

      self.histoSep = QLabel()
      self.histoMix = QLabel()

      self.jacc = QLabel()
      self.lda = QLabel()

      self.pears = QLabel()
      self.pearsFormula = QLabel()
      self.pearsonFormula = QPixmap('images/pearson_formula.png')
      self.pearsonFormula = self.pearsonFormula.scaledToWidth(int((self.size.width())/4))
      self.pearsFormula.setPixmap(self.pearsonFormula)
      self.pearsFormula.setFixedSize(800, 300)
      self.pears2 = QLabel()

      self.scrollBar1 = QScrollArea()
      self.scrollBar1a = QScrollArea()
      #/self.scrollBar1.setFixedSize(self.size.width(), 300)

      self.scrollBar2 = QScrollArea()
      self.scrollBar2a = QScrollArea()
      #self.scrollBar1.horizontalScrollBar().setStyleSheet("color:blue;background-color:red;")

      self.scrollBar3 = QScrollArea()
      self.scrollBar3a = QScrollArea()
      self.scrollBar3b = QScrollArea()
      self.scrollBar3c = QScrollArea()

      self.scrollBar4 = QScrollArea()
      self.scrollBar4a = QScrollArea()

      self.menuLayout.addWidget(self.logo)
      self.menuLayout.addWidget(self.query)
      self.menuLayout.addWidget(self.lineQuery)
      self.separator()
      self.menuLayout.addWidget(self.submissions)
      self.menuLayout.addWidget(self.lineSubmission)
      self.separator()
      self.menuLayout.addWidget(self.comments)
      self.menuLayout.addWidget(self.lineComments)
      self.separator()
      self.menuLayout.addWidget(self.subReddit)
      self.menuLayout.addWidget(self.comboSubReddit)
      self.menuLayout.addWidget(self.submit)

      self.errorMsg.addWidget(self.error)

      self.buttonsLayout.addWidget(self.buttonHistoSep)
      self.buttonsLayout.addWidget(self.buttonHistoMix)
      self.buttonsLayout.addWidget(self.buttonJaccard)
      self.buttonsLayout.addWidget(self.buttonPearson)

      self.page_layout.addStretch()
      self.page_layout.insertLayout(self.page_layout.count()-1, self.menuLayout)
      self.page_layout.insertLayout(self.page_layout.count()-1, self.errorMsg)
      self.page_layout.insertLayout(self.page_layout.count()-1, self.buttonsLayout)
      #self.page_layout.addLayout(self.stackLayout)
      #self.page_layout.addLayout(self.contentLayout1)
      #/self.page_layout.addWidget(self.scrollbar1)
      #/self.page_layout.addLayout(self.contentLayout2)

      #/self.w.setGeometry(0, 0, self.size.width(), int(self.size.height()-self.size.height()/2))
      self.w.showMaximized()
      self.w.setLayout(self.page_layout)
      self.showMaximized()
      self.show()

   def separator(self):
      dot = QLabel(self)
      logoDot = QPixmap('images/white_dot.png')
      logoDot = logoDot.scaledToWidth(int((self.size.width())/95))
      dot.setPixmap(logoDot)
      dot.setFixedSize(25, 30)
      self.menuLayout.addWidget(dot)

   def clicked(self):
      self.isSubmit = True
      QApplication.setOverrideCursor(Qt.WaitCursor)
      print("je clique")
      self.boolError = False
      self.error.setText("Processing... (it may take some time)")
      self.widthError = self.error.fontMetrics().boundingRect(self.error.text()).width()
      self.error.resize(int(self.size.width()), 30)
      self.error.setAlignment(Qt.AlignCenter)
      self.error.setFont(QFont("Calibri", 14))
      self.error.setStyleSheet("color:white;background-color:black;")
      self.error.move(int(self.size.width()/2 - self.widthError/2), int(self.size.height()/10))
      
      if(self.contentLayout1.count() >= 1):
         self.deleteContent(self.contentLayout1)
         self.deleteContent(self.contentLayout1a)
         self.deleteContent(self.contentLayout2)
         self.deleteContent(self.contentLayout2a)
         self.deleteContent(self.contentLayout3)
         self.deleteContent(self.contentLayout3a)
         self.deleteContent(self.contentLayout3b)
         self.deleteContent(self.contentLayout3c)
         self.deleteContent(self.contentLayout4)
         self.deleteContent(self.contentLayout4a)

      self.w.repaint()
      query = self.getQuery()
      submission = self.getSubmission()
      comments = self.getComments()
      subReddit = self.getSubReddit()
      if self.contentLayout1.count() >= 1:
         self.scrollBar1.deleteLater()
         self.scrollBar1a.deleteLater()
         self.scrollBar2.deleteLater()
         self.scrollBar2a.deleteLater()
         self.scrollBar3.deleteLater()
         self.scrollBar3a.deleteLater()
         self.scrollBar3b.deleteLater()
         self.scrollBar3c.deleteLater()
         self.scrollBar4.deleteLater()
         self.scrollBar4a.deleteLater()

      if query == '' or submission == '' or comments == '':
         self.boolError = True
         self.error.setText("All fields must be filled!")
      else:
         submission = int(self.getSubmission())
         comments = int(self.getComments())
         if(submission == 0 or comments == 0):
            self.boolError = True
            self.error.setText("You must search for at least 1 submission and 1 comment!")
         elif comments < 5:
            self.boolError = True
            self.error.setText("You must put at least 5 comments to get good results.")
         else:
            subColl = SubmissionCollection(submission, comments, query, subReddit)

            histSep = separateOverlapSubCommentHists(subColl)
            if histSep == "Not much comments" or histSep == "No comments" or histSep == []:
               self.boolError = True
               self.error.setText("Not enough comments are available. Please choose another SubReddit or send a new request.")
            else:
               self.histoSep.setText("The separated histograms display the most popular word occurrences of a submission's article and comments.<br>Each graph is composed of subplot histogram, one for each comment of a single submission.<br>")
               self.histoSep.setFont(QFont("Calibri", 14))
               self.histoSep.setStyleSheet("color:white;")
               self.contentLayout1.addWidget(self.histoSep)
               self.contentLayout1.setSizeConstraint(3)
               self.scrollBar1 = self.scrollAreaToLayout(self.contentLayout1)
               self.scrollBar1.setFixedHeight(115)
               self.scrollBar1.setDisabled(True)
               self.scrollBar1.verticalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
               self.page_layout.insertWidget(self.page_layout.count()-1, self.scrollBar1)
               for fig in histSep:
                  print(fig)
                  self.contentLayout1a.addWidget(self.createLabelFromFigure(fig))
               self.contentLayout1a.setSizeConstraint(3)
               self.scrollBar1a = self.scrollAreaToLayout(self.contentLayout1a)
               self.scrollBar1a.setFixedHeight(550)
               self.page_layout.insertWidget(self.page_layout.count()-1, self.scrollBar1a)

               histMix = mixedOverlapSubCommentHists(subColl)
               self.histoMix.setText("The mixed histograms display the most popular word occurrences of a submission's article and comments.<br>Each graph is composed of a histogram selecting words of every comment of a single submission.<br>")
               self.histoMix.setFont(QFont("Calibri", 14))
               self.histoMix.setStyleSheet("color:white;")
               self.contentLayout2.addWidget(self.histoMix)
               self.contentLayout2.setSizeConstraint(3)
               self.scrollBar2 = self.scrollAreaToLayout(self.contentLayout2)
               self.scrollBar2.setFixedHeight(115)
               self.scrollBar2.setDisabled(True)
               self.scrollBar2.verticalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
               self.page_layout.insertWidget(self.page_layout.count()-1, self.scrollBar2)
               for fig in histMix:
                  self.contentLayout2a.addWidget(self.createLabelFromFigure(fig))
               self.contentLayout2a.setSizeConstraint(3)
               self.scrollBar2a = self.scrollAreaToLayout(self.contentLayout2a)
               self.scrollBar2a.setFixedHeight(550)
               self.page_layout.insertWidget(self.page_layout.count()-1, self.scrollBar2a)

               jaccCoeff = calculateJacquard(subColl)
               self.jacc.setText("The <b>Jaccard index</b> (or <b>Jaccard similarity coefficient</b>) is a statistic which is used to measure the similarity between 2 samples.<br>For each submission, the Jaccard index is calculated between the 20 most frequent words in the article and its comments.<br>This coefficient is between 0 and 1. The closer it is to 1, the more similar the article and its comments are.<br>")
               self.jacc.setFont(QFont("Calibri", 14))
               self.jacc.setStyleSheet("color:white;")
               self.contentLayout3.addWidget(self.jacc)
               self.contentLayout3.setSizeConstraint(3)
               self.scrollBar3 = self.scrollAreaToLayout(self.contentLayout3)
               self.scrollBar3.setFixedHeight(115)
               self.scrollBar3.setDisabled(True)
               self.scrollBar3.verticalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
               self.page_layout.insertWidget(self.page_layout.count()-1, self.scrollBar3)
               for coeff in range(len(jaccCoeff)):
                  text = "Submission " + str(coeff+1) + ":  " + str(jaccCoeff[coeff])
                  self.contentLayout3a.addWidget(self.createLabel(text))
               self.contentLayout3a.setSizeConstraint(7)
               self.scrollBar3a = self.scrollAreaToLayout(self.contentLayout3a)
               self.scrollBar3a.setFixedHeight(int(self.size.height()/4.1))
               self.page_layout.insertWidget(self.page_layout.count()-1, self.scrollBar3a)

               jaccLDA = performLDA(subColl)
               self.lda.setText("<b>LDA </b> (or <b>Latent Dirichlet Allocation</b>) is a statistical model for topic modeling methods.<br>The LDA model will define from a document 3 topics each containing 5 frequent words. This model will be repeated on 2 different documents: the article and the set of selected comments.<br>The Jaccard index is computed between the different topics obtained by the LDA model for the article and for the comments.<br>")
               self.lda.setFont(QFont("Calibri", 14))
               self.lda.setStyleSheet("color:white;")
               self.contentLayout3b.addWidget(self.lda)
               self.contentLayout3b.setSizeConstraint(3)
               self.scrollBar3b = self.scrollAreaToLayout(self.contentLayout3b)
               self.scrollBar3b.setFixedHeight(115)
               self.scrollBar3b.setDisabled(True)
               self.scrollBar3b.verticalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
               self.page_layout.insertWidget(self.page_layout.count()-1, self.scrollBar3b)
               for coeff in range(len(jaccLDA)):
                  text = "Submission " + str(coeff+1) + ":  " + str(jaccLDA[coeff])
                  self.contentLayout3c.addWidget(self.createLabel(text))
               self.contentLayout3c.setSizeConstraint(7)
               self.scrollBar3c = self.scrollAreaToLayout(self.contentLayout3c)
               self.scrollBar3c.setFixedHeight(int(self.size.height()/4.1))
               self.page_layout.insertWidget(self.page_layout.count()-1, self.scrollBar3c)

               pearson = pearsonCorrelation(subColl)
               self.pears.setText("The <b>Pearson correlation</b> is a statistical method used to measure the index reflecting a linear relationship between two sets of data. The coefficient is obtained using this formula:")
               self.pears.setFont(QFont("Calibri", 14))
               self.pears.setStyleSheet("color:white;")
               self.pears2.setText("The correlation coefficient varies between -1 and 1. A negative value means that when one variable increases, the other decreases. In contrast, a positive correlation indicates that the two variables vary together in the same direction. Pearson correlations will be calculated between the sentiment associated with the article and that of the selected comments. The results are written in this form: (Pearson correlation coefficient, P-value or the probability of finding the result).")
               self.pears2.setFont(QFont("Calibri", 14))
               self.pears2.setStyleSheet("color:white;")
               self.pears2.setWordWrap(True)
               self.contentLayout4.addWidget(self.pears)
               self.contentLayout4.addWidget(self.pearsFormula)
               self.contentLayout4.addWidget(self.pears2)
               self.contentLayout4.setSizeConstraint(6)
               self.scrollBar4 = self.scrollAreaToLayout(self.contentLayout4)
               self.scrollBar4.setFixedHeight(int(self.size.height()/2.3))
               self.scrollBar4.setDisabled(True)
               self.scrollBar4.verticalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
               self.page_layout.insertWidget(self.page_layout.count()-1, self.scrollBar4)
               for coeff in range(len(pearson)):
                  text = "Submission " + str(coeff+1) + ":  " + str(pearson[coeff])
                  self.contentLayout4a.addWidget(self.createLabel(text))
               self.contentLayout4a.setSizeConstraint(8)
               self.scrollBar4a = self.scrollAreaToLayout(self.contentLayout4a)
               self.scrollBar4a.setFixedHeight(int(self.size.height()/4))
               self.page_layout.insertWidget(self.page_layout.count()-1, self.scrollBar4a)

               self.getHistoSep()
               

      QApplication.restoreOverrideCursor()

      if self.boolError == True:
         self.widthError = self.error.fontMetrics().boundingRect(self.error.text()).width()
         self.error.setFixedSize(self.widthError + 40, 30)
         self.error.setAlignment(Qt.AlignCenter)
         self.error.setFont(QFont("Calibri", 14))
         self.error.setStyleSheet("color:white;background-color:#ff4500;border-radius:4px;")
         self.error.move(int(self.size.width()/2 - self.widthError/2), int(self.size.height()/10))
         self.buttonHistoSep.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
         self.buttonHistoMix.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
         self.buttonJaccard.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
      else:
         self.error.setText("")
         self.repaint()


   def getQuery(self):
      return self.lineQuery.text()
   
   def getSubmission(self):
      return self.lineSubmission.text()

   def getComments(self):
      return self.lineComments.text()

   def getSubReddit(self):
      return self.comboSubReddit.currentText()

   def figureToQImage(self, fig):
      canvas = FigureCanvas(fig)
      canvas.draw()
      size = canvas.size()
      width, height = size.width(), size.height()
      im = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
      return im

   def scrollAreaToLayout(self, layout):
      self.widget = QWidget()
      self.scrollbar = QScrollArea()
      if type(layout) == QHBoxLayout:
         self.scrollbar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
         self.scrollbar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
      else:
         self.scrollbar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
         self.scrollbar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
      self.scrollbar.setWidgetResizable(True)
      self.widget.setLayout(layout)
      self.scrollbar.setWidget(self.widget)
      self.scrollbar.hide()
      return self.scrollbar

   def createLabelFromFigure(self, fig):
      label = QLabel()
      im = self.figureToQImage(fig)
      label.setPixmap(QPixmap(im))
      label.resize(640, 480)
      return label
   
   def createLabel(self, text):
      label = QLabel()
      label.setText(text)
      label.setFont(QFont("Calibri", 14))
      label.setStyleSheet("color:white;background-color:black")
      return label
   
   def getHistoSep(self):
      if self.isSubmit == True and self.boolError == False:
         self.scrollBar1.show()
         self.scrollBar1a.show()
         self.scrollBar2.hide()
         self.scrollBar2a.hide()
         self.scrollBar3.hide()
         self.scrollBar3a.hide()
         self.scrollBar3b.hide()
         self.scrollBar3c.hide()
         self.scrollBar4.hide()
         self.scrollBar4a.hide()
         self.buttonHistoSep.setStyleSheet("color:white;background-color:#ff4500;border-radius:4px;")
         self.buttonHistoMix.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
         self.buttonJaccard.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
         self.buttonPearson.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
      else: 
         self.error.setText("Please send a submission.")
         self.widthError = self.error.fontMetrics().boundingRect(self.error.text()).width()
         self.error.setFixedSize(self.widthError + 40, 30)
         self.error.setAlignment(Qt.AlignCenter)
         self.error.setFont(QFont("Calibri", 14))
         self.error.setStyleSheet("color:white;background-color:#ff4500;border-radius:4px;")
         self.error.move(int(self.size.width()/2 - self.widthError/2), int(self.size.height()/10))

   def getHistoMix(self):
      if self.isSubmit == True and self.boolError == False:
         self.scrollBar1.hide()
         self.scrollBar1a.hide()
         self.scrollBar2.show()
         self.scrollBar2a.show()
         self.scrollBar3.hide()
         self.scrollBar3a.hide()
         self.scrollBar3b.hide()
         self.scrollBar3c.hide()
         self.scrollBar4.hide()
         self.scrollBar4a.hide()
         self.buttonHistoSep.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
         self.buttonHistoMix.setStyleSheet("color:white;background-color:#ff4500;border-radius:4px;")
         self.buttonJaccard.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
         self.buttonPearson.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
      else: 
         self.error.setText("Please send a submission.")
         self.widthError = self.error.fontMetrics().boundingRect(self.error.text()).width()
         self.error.setFixedSize(self.widthError + 40, 30)
         self.error.setAlignment(Qt.AlignCenter)
         self.error.setFont(QFont("Calibri", 14))
         self.error.setStyleSheet("color:white;background-color:#ff4500;border-radius:4px;")
         self.error.move(int(self.size.width()/2 - self.widthError/2), int(self.size.height()/10))

   def getJaccardIndex(self):
      if self.isSubmit == True and self.boolError == False:
         self.scrollBar1.hide()
         self.scrollBar1a.hide()
         self.scrollBar2.hide()
         self.scrollBar2a.hide()
         self.scrollBar3.show()
         self.scrollBar3a.show()
         self.scrollBar3b.show()
         self.scrollBar3c.show()
         self.scrollBar4.hide()
         self.scrollBar4a.hide()
         self.buttonHistoSep.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
         self.buttonHistoMix.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
         self.buttonJaccard.setStyleSheet("color:white;background-color:#ff4500;border-radius:4px;")
         self.buttonPearson.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
      else: 
         self.error.setText("Please send a submission.")
         self.widthError = self.error.fontMetrics().boundingRect(self.error.text()).width()
         self.error.setFixedSize(self.widthError + 40, 30)
         self.error.setAlignment(Qt.AlignCenter)
         self.error.setFont(QFont("Calibri", 14))
         self.error.setStyleSheet("color:white;background-color:#ff4500;border-radius:4px;")
         self.error.move(int(self.size.width()/2 - self.widthError/2), int(self.size.height()/10))

   def getPearsonCorrelation(self):
      if self.isSubmit == True and self.boolError == False:
         self.scrollBar1.hide()
         self.scrollBar1a.hide()
         self.scrollBar2.hide()
         self.scrollBar2a.hide()
         self.scrollBar3.hide()
         self.scrollBar3a.hide()
         self.scrollBar3b.hide()
         self.scrollBar3c.hide()
         self.scrollBar4.show()
         self.scrollBar4a.show()
         self.buttonHistoSep.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
         self.buttonHistoMix.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
         self.buttonJaccard.setStyleSheet("color:white;background-color:#3b3b45;border-radius:4px;")
         self.buttonPearson.setStyleSheet("color:white;background-color:#ff4500;border-radius:4px;")
      else: 
         self.error.setText("Please send a submission.")
         self.widthError = self.error.fontMetrics().boundingRect(self.error.text()).width()
         self.error.setFixedSize(self.widthError + 40, 30)
         self.error.setAlignment(Qt.AlignCenter)
         self.error.setFont(QFont("Calibri", 14))
         self.error.setStyleSheet("color:white;background-color:#ff4500;border-radius:4px;")
         self.error.move(int(self.size.width()/2 - self.widthError/2), int(self.size.height()/10))

   def deleteContent(self, layout):
      index = layout.count()
      for i in range(index):
         print(layout.itemAt(i))
         widget = layout.itemAt(i).widget()
         widget.deleteLater()
         i += 1

def main():
   app = QApplication(sys.argv)
   gui = Gui()
   sys.exit(app.exec_()) 

if __name__ == '__main__':
   main()