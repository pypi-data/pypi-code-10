import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import SGD, adam, RMSprop, adagrad, Adadelta
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Convolution1D, MaxPooling1D, Convolution2D, MaxPooling2D
from keras.layers.advanced_activations import PReLU
from keras.layers.recurrent import LSTM, GRU
from keras.utils import np_utils
from keras.regularizers import l2
from keras.callbacks import ModelCheckpoint, EarlyStopping
import matlab.engine
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.cross_validation import cross_val_predict, StratifiedKFold, permutation_test_score
from sklearn import cross_validation, svm, metrics
import theano
import time
import imp
import sys

from ECoG_Decoding.Decode import ModelMaker

def Decode(X, Y, nb_classes, ChannelOfInterest, Events, Times, WhatToDecode, nbArtificialSamples, DownsampleFq, FilterData, nbCvFolds, locutoff, hicutoff, nmodels, shufflelabels,earlystopping, VisModelTestAud, subject, verbosity, savefile, filename, Experiment_dir ):


    AlldataX = X
    AlldataY = Y
    nTrialsOrig = AlldataX.shape[0]
    dims = AlldataX.shape[1]
    feats = AlldataX.shape[2]

    
    eng = matlab.engine.start_matlab()
    
    Accuracy=[]
    Predictions=[]
    Predictions_unweighted=[]
    Predictions_TopBagModel=[]
    Accuracy_unweighted=[]
    Accuracy_TopBagModel=[]
    TestLabels=[]
    Predictions_flattened=[]
    TestLabels_flattened=[]
    AllScores_test = []
    AllScores_validate=[]
    Fold=1
    
    #kfolds = StratifiedKFold(np.squeeze(AlldataY.astype(int)), n_folds=nbCvFolds) 
    kfolds = cross_validation.ShuffleSplit(nTrialsOrig, n_iter=nbCvFolds, test_size=0.2,random_state=0)
    
    for train, test in kfolds:
        print("Fold %s of %s..."%(Fold,nbCvFolds))
            
        X_train_fold = AlldataX[train]
        X_test_fold = AlldataX[test]
        Y_train_fold = AlldataY[train]
        Y_test_fold = AlldataY[test]
        
        #if VisModelTestAud==1:
            #X_test_fold = AudDataX[test]
            #Y_test_fold = AudDataY[test]
            
        X_train_bag_temp, X_validate_bag, Y_train_bag_temp, Y_validate_bag = cross_validation.train_test_split(X_train_fold, Y_train_fold, test_size=.1) #Subdivide train to validation set
            
        X_train_toMatlab = matlab.double(np.array(X_train_bag_temp).tolist())
        Y_train_toMatlab = matlab.double(np.array(Y_train_bag_temp).tolist())
    
        ##Generate new artificial trials
        Output = eng.GenNewTrainset(X_train_toMatlab, Y_train_toMatlab, nbArtificialSamples, shufflelabels, async=True, nargout=2)
        Result = Output.result()   
        X_train_bag = np.float32(np.array(Result[0][::]))
        if len(ChannelOfInterest) == 1:
            X_train_bag = X_train_bag[...,np.newaxis]
        Y_train_bag = np.array(Result[1][::])
        del Result
            
        X_validate_bag =  np.float32(X_validate_bag)   
        X_test_bag=np.float32(X_test_fold)
        Y_test_bag=Y_test_fold
        
        if shufflelabels==1:
            Y_train_bag = np.random.permutation(Y_train_bag)
                    
        y_train_bag = np.float32(np_utils.to_categorical(Y_train_bag, nb_classes))
        y_validate_bag = np.float32(np_utils.to_categorical(Y_validate_bag, nb_classes))
        y_test_bag = np.float32(np_utils.to_categorical(Y_test_bag, nb_classes))
        
        
        ## Bagging  
        from keras.utils.layer_utils import print_layer_shapes
        
        probs_bags = []
        probs_bags_unweighted = []
        bag_score = []
        bag_validation_score = []
        for bag in xrange(nmodels):
            t=time.time()
            print 'Bag %s out of %s' % (bag+1, nmodels)
            model = ModelMaker.makemodel(dims,feats,nb_classes,bag+1)
            #plot(model, 'model.png')
            weights = model.get_weights()
            state = model.optimizer.get_state()
            
            
            #Initialize and train  
            #print_layer_shapes(model,input_shapes=(X_train_bag.shape))
            model.set_weights(weights)
            model.optimizer.set_state(state)
            if not os.path.exists(os.path.join(Experiment_dir, "ModelWeights")):
                os.makedirs(os.path.join(Experiment_dir, "ModelWeights"))

            checkpointer = ModelCheckpoint(filepath=os.path.join(Experiment_dir,"ModelWeights","weights.hdf5"), monitor='val_loss', verbose=1, save_best_only=True, mode='auto')
            early_stopping= EarlyStopping(patience=50,verbose=1)
            if earlystopping==1:
                model.fit(X_train_bag, y_train_bag, nb_epoch=50, batch_size=512 ,validation_data=(X_validate_bag, y_validate_bag),verbose=verbosity, show_accuracy=True, callbacks=[checkpointer, early_stopping])  
                model.load_weights(os.path.join(Experiment_dir,"ModelWeights", "weights.hdf5"))
            elif earlystopping==0:
                model.fit(X_train_bag, y_train_bag, nb_epoch=50, batch_size=512 ,validation_data=(X_validate_bag, y_validate_bag),verbose=verbosity, show_accuracy=True)  
                            
            validation_score =  model.evaluate(X_validate_bag, y_validate_bag, show_accuracy=True, verbose=0)  
            score= model.evaluate(X_test_bag, y_test_bag, show_accuracy=True, verbose=0)  
            elapsed = time.time()-t
            print 'Validation score: %s, accuracy: %s' % (validation_score[0], validation_score[1])
            print 'Test score: %s, accuracy: %s' % (score[0], score[1])
            print 'Training time: %s' % elapsed
            sys.stdout.flush() #flush output to make sure it's printing 
            bag_score.append(score[1])
            bag_validation_score.append(validation_score[1])
            AllScores_test.append(score)
            
            
            probs_unweighted = np_utils.to_categorical(model.predict_classes(X_test_bag,batch_size=128,verbose=0), nb_classes) 
            #probs_unweighted = model.predict(X_test_fold,batch_size=128,verbose=1)
            probs_bags_unweighted.append(probs_unweighted)      
            probs = np.multiply(probs_unweighted, (validation_score[1]*10))
            probs_bags.append(probs)
    
        
        #Have the top performing model vote three times                       
        bag_score = np.array(bag_score)
        bag_validation_score = np.array(bag_validation_score)
        TopBag = bag_validation_score.argmax(axis=0)
        TopBagWeighted = probs_bags_unweighted
        TopBagWeighted.append(probs_bags_unweighted[TopBag])
        TopBagWeighted.append(probs_bags_unweighted[TopBag])
    
                    
        probs_BagMean = np.mean(np.array(probs_bags),axis=0)
        probs_unweighted_BagMean = np.mean(np.array(probs_bags_unweighted),axis=0)
        probs_TopBagModel = np.mean(np.array(TopBagWeighted),axis=0)
        BaggedPredictions = probs_BagMean.argmax(axis=1)
        BaggedPredictions_unweighted = probs_unweighted_BagMean.argmax(axis=1)
        BaggedPredictions_TopBagModel = probs_TopBagModel.argmax(axis=1)
        Bag_accuracy = accuracy_score(Y_test_bag, BaggedPredictions)
        Bag_accuracy_unweighted = accuracy_score(Y_test_bag, BaggedPredictions_unweighted)
        Bag_accuracy_TopBagModel = accuracy_score(Y_test_bag, BaggedPredictions_TopBagModel)
        print 'Fold Accuracy: Unweighted - %s, Weighted - %s, TopBagModel - %s' % (Bag_accuracy_unweighted, Bag_accuracy, Bag_accuracy_TopBagModel)
    
        Predictions.append(BaggedPredictions)
        Predictions_unweighted.append(BaggedPredictions_unweighted)
        Predictions_TopBagModel.append(BaggedPredictions_TopBagModel)
        TestLabels.append(Y_test_bag)
        Accuracy.append(Bag_accuracy)
        Accuracy_unweighted.append(Bag_accuracy_unweighted)
        Accuracy_TopBagModel.append(Bag_accuracy_TopBagModel)
        
        Fold=Fold+1
        
    
    
    #############  
    AllScores = np.array(AllScores_test)[:,1]  
    Predictions_flattened= [val for sublist in Predictions_unweighted for val in sublist]
    TestLabels_flattened=[val for sublist in TestLabels for val in sublist]
    
    if savefile==1:
        import pickle
        import os
        if not os.path.exists(os.path.join(Experiment_dir,"out", "%s" % subject)):
            os.makedirs(os.path.join(Experiment_dir,"out", "%s" % subject))
            
        os.chdir(os.path.join(Experiment_dir,"out", "%s" % subject))
        pickle.dump((Accuracy, Predictions_flattened, TestLabels_flattened, AllScores, Accuracy_unweighted, Predictions_unweighted, Predictions), open(filename, "wb"))
    
    return (Accuracy, Predictions_flattened, TestLabels_flattened, AllScores, Accuracy_unweighted, Predictions_unweighted, Predictions)
    
    
    