'''
Created on Feb 20, 2015

@author: Mohit
'''
import sentiment as ck

#sentence with positive words and result is positive.
ck.print_sentiment('well done. good job')

#sentence with negative word - horrible but result is positive.
ck.print_sentiment('there are cool freatures but still it is horrible.')

#sentence with positive word - Awesome but result is neutral.
ck.print_sentiment('the movie was Awesome')
