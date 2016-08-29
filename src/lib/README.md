###Lib Model Classifications

##### KNeighborsClassifier
- macro precision =  0.967558265525  macro recall =  0.96719858156

---> Matrix Confusion ===>: 
[[351  25   0]
 [ 12 364   0]
 [  0   0 188]]
---> Best Parameter Classification [ best parameter:  KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
           metric_params=None, n_neighbors=10, p=2, weights='distance') , best params:  {'weights': 'distance', 'n_neighbors': 10} ]

##### RandomForestClassifier
- macro precision =  0.972623773235  macro recall =  0.972517730496

---> Matrix Confusion ===>: 
[[364  12   0]
 [ 19 357   0]
 [  0   0 188]]
 ---> Best Parameter Classification [ best parameter:  RandomForestClassifier(bootstrap=True, class_weight=None, criterion='entropy',
            max_depth=None, max_features='auto', max_leaf_nodes=None,
            min_samples_leaf=1, min_samples_split=2,
            min_weight_fraction_leaf=0.0, n_estimators=200, n_jobs=-1,
            oob_score=False, random_state=None, verbose=0,
            warm_start=False) , best params:  {'n_estimators': 200} ]

##### GradientBoostingClassifier
- macro precision =  0.946957556166  macro recall =  0.947695035461

---> Matrix Confusion ===>: 
[[341  34   1]
 [ 24 352   0]
 [  0   0 188]]
---> Best Parameter Classification [ best parameter:  GradientBoostingClassifier(init=None, learning_rate=0.1, loss='deviance',
              max_depth=3, max_features=None, max_leaf_nodes=None,
              min_samples_leaf=1, min_samples_split=2,
              min_weight_fraction_leaf=0.0, n_estimators=400,
              random_state=0, subsample=1.0, verbose=0, warm_start=False) , best params:  {'n_estimators': 400, 'max_depth': 3, 'learning_rate': 0.1} ]

##### AdaBoostClassifier
- macro precision =  0.851677843967  macro recall =  0.841312056738

---> Matrix Confusion ===>: 
[[242 134   0]
 [ 45 331   0]
 [  0   0 188]]
---> Best Parameter Classification [ best parameter:  AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None,
          learning_rate=0.01, n_estimators=50, random_state=None) , best params:  {'n_estimators': 50, 'learning_rate': 0.01} ]
