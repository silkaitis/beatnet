# Intro

The number of new Drum and Bass songs released each year on
[Beatport](http://pro.beatport.com) has grown significantly
over the last decade. The growth can be attributed to anything from the
rise of digital DJing to increased access to music publishing platforms
to more music production tools available.

![New Releases per Year](https://s3-us-west-2.amazonaws.com/daniusdonuts/data_blog/nrp/dnb_per_year.png)
Source: Beatport API

This explosion of new music can be a blessing and curse for the
casual DJ, like myself. Although, it is easy for DJs to differentiate
themselves due to sheer volume of choices, it's nearly impossible to
sift through all the possibilities making it difficult to not miss
a new favorite or "hidden gem". On Beatport, each release has a
2 minute snippet that can be reviewed prior to purchasing.
In 2016, it would take 994 hours to review each release in its
entirety (19 hours a week on average). Hence the dilemma.
Releases can be filtered by favorite artists or record labels but
that can lead to a homogenous collection. Who wants to listen to the
same 10 artists each week?

There is an opportunity to automate the assessment of each release
through machine learning. The concept is to build a model to predict
the probability that a new release aligns with an existing collection
of music. An initial thought is to use a recommender system but I do
not have access to the needed data. Instead, I'll build a model
from features extracted from the 2 minute audio snippets created by
Beatport. The snippets are consistent in length and position within the
full song thus simplifying any audio analysis.
The first project phase to harmonize my collection with
Beatport's track IDs is complete. I won't detail the nuances of this
initial data cleaning since the next project phases will be more
interesting.
