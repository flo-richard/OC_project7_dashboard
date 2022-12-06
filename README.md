# OC_project7_dashboard

This dashboard is a banking application used to determine whether a client will be able to repay a credit, based on a Machine Learning model. The details of the training of this model can be found at https://github.com/flo-richard/OpenClassrooms_Project7_main .

It is an interactive prompt UI where only the client Id within the bank data base is required. The Id is then stored as a .json file and sent to a non-interactive API (see details at https://github.com/flo-richard/OpenClassrooms_project7_api) which will compute the decision and different explanations regarding this decision. The decision and explanations are then sent back to the dashboard and displayed live.

KEYWORDS : API, Interactive dashboard
