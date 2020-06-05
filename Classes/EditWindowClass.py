from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from Classes.QToasterClass import QToaster
from datetime import datetime
import mysql.connector

class EditForm_Win(QDialog):
    def __init__(self, *args, **kwargs):
        super(EditForm_Win, self).__init__()    #*args and *kwargs removed from super init
        self.ui = uic.loadUi('UI Files/EditMovieForm.ui', self)   #Loads Edit Movie Form Window

        #Definitions for add form entry fields
        self.submitButton = self.findChild(QtWidgets.QPushButton, 'SubmitButton')
        self.submitButton.clicked.connect(self.updateMovie)
        self.cancelButton = self.findChild(QtWidgets.QPushButton, 'CancelEntryButton')
        self.cancelButton.clicked.connect(self.close)

        self.titleVal = self.findChild(QtWidgets.QLineEdit, 'MovieTitleEntry')
        self.dateVal = self.findChild(QtWidgets.QDateEdit, 'DateWatchedEntry')
        self.ratingVal = self.findChild(QtWidgets.QComboBox, 'MovieRatingEntry')
        self.genreVal = self.findChild(QtWidgets.QComboBox, 'MovieGenreEntry')
        self.theaterChecked = self.findChild(QtWidgets.QRadioButton, 'MovieLocationTheaterEntry')
        self.homeChecked = self.findChild(QtWidgets.QRadioButton, 'MovieLocationHomeEntry')
        self.commentVal = self.findChild(QtWidgets.QPlainTextEdit, 'MovieCommentsEntry')
        self.errorMessage = ""
        self.locationVal = ""

        #Populates edit form with current entry info
        self.parentWin = args[0]
        self.entryIdVal = args[1]
        self.titleVal.setText(args[2])
        self.dateVal.setDate((datetime.strptime(args[3], '%Y-%m-%d')).date())  #Converts date string to date object
        self.ratingVal.setCurrentText(args[4])
        self.genreVal.setCurrentText(args[5])
        self.locationVal = args[6]
        self.commentVal.setPlainText(args[7])
        self.curRow = args[8]
        if(self.locationVal == 'Home'):
            self.homeChecked.setChecked(True)
        elif(self.locationVal == 'Theater'):
            self.theaterChecked.setChecked(True)

        self.parent().changed = False #Makes sure that change flag is false initially

    def updateMovie(self):
        #Updates a movie entry
        dbConnection2 = self.parentWin.dbConnection
        if self.validateSubmission() == True:
            sql = "UPDATE log SET LOG_MOVIE_TITLE = %s, LOG_MOVIE_DATE = %s, LOG_MOVIE_RATING = %s, LOG_MOVIE_GENRE = %s, LOG_MOVIE_LOCATION = %s, LOG_MOVIE_COMMENTS = %s WHERE LOG_ID = %s"
            vals = [self.titleVal.text(), self.dateVal.date().toString('yyyy-MM-dd'), self.ratingVal.currentText(), self.genreVal.currentText(), self.locationVal, self.commentVal.toPlainText(), self.entryIdVal] 
            cursor = dbConnection2.cursor()
            cursor.execute(sql, vals)
            dbConnection2.commit()
            cursor.close()

            QToaster.showMessage(self.parentWin, 'Entry Updated', corner=QtCore.Qt.BottomRightCorner)
            self.parent().changed = True
            self.close()
        else:
            print("Error: " + self.errorMessage)

    def validateSubmission(self):
        #Ensures that there are not errors with the movie entry being edited
        if self.titleVal.text() == "" or self.titleVal.text() == None:
            self.errorMessage = "Please Enter a Title"
            QToaster.showMessage(self.parentWin, self.errorMessage, corner=QtCore.Qt.BottomRightCorner)
            return False
        if len(self.titleVal.text()) >= 100:
            self.errorMessage = "Title is too long" #Don't really love the way this is phrased, will probably revise this later
            QToaster.showMessage(self.parent(), self.errorMessage, corner=QtCore.Qt.BottomRightCorner)
            return False
        if self.dateVal.date().toString() == None:
            self.errorMessage = "Please Enter a Date"
            QToaster.showMessage(self.parentWin, self.errorMessage, corner=QtCore.Qt.BottomRightCorner)
            return False
        if self.ratingVal.currentText() == None:
            self.errorMessage = "Please Enter a Rating"
            QToaster.showMessage(self.parentWin, self.errorMessage, corner=QtCore.Qt.BottomRightCorner)
            return False
        if self.genreVal.currentText() == None:
            self.errorMessage = "Please Enter a Genre"
            QToaster.showMessage(self.parentWin, self.errorMessage, corner=QtCore.Qt.BottomRightCorner)
            return False

        if self.theaterChecked.isChecked() == True: 
            self.locationVal = "Theater"
        elif self.homeChecked.isChecked() == True:
            self.locationVal = "Home"
        else:
            self.locationVal = None

        return True 

        
        
