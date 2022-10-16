# OC_project7_dashboard

This dashboard is a banking application used to determine whether a client will be able to repay a credit, based on a Machine Learning model. The details of the training of this model can be found at https://github.com/flo-richard/OpenClassrooms_Projet7 .
It is an interactive prompt UI where the client will fill out a form with different information. This form is then stored as a json file and sent to a non-interactive API (see details at https://github.com/flo-richard/scoring_model_api) which will compute the decision and different explanations regarding this decision. The details of this API can be found at  .

Both the API and the dashboard are deployed as heroku applications :
API : https://scoring-oc7.herokuapp.com/getPrediction
Dashboard : https://credit-score-dashboard-oc7.herokuapp.com/