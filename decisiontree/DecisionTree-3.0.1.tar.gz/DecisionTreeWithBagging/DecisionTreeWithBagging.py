
from DecisionTree import DecisionTree

import re
import random
import operator
from functools import reduce


def convert(value):
    try:
        answer = float(value)
        return answer
    except:
        return value

def sample_index(sample_name):
    '''
    When the training data is read from a CSV file, we assume that the first column
    of each data record contains a unique integer identifier for the record in that
    row. This training data is stored in a dictionary whose keys are the prefix
    'sample_' followed by the identifying integers.  For the data in the old-style
    `.dat' files, we assume that each record begins with the string `sample_xx' where
    `xx' is a unique integer.  In both cases, the purpose of this function is to
    return the identifying integer associated with a data record.
    '''
    m = re.search('_(.+)$', sample_name)
    return int(m.group(1))
    
class DecisionTreeWithBagging(object):

    def __init__(self, *args, **kwargs ):
        if kwargs and args:
            raise ValueError(  
                   '''DecisionTreeWithBagging constructor can only be called with keyword arguments for
                      the following keywords: training_datafile, entropy_threshold,
                      max_depth_desired, csv_class_column_index,
                      symbolic_to_numeric_cardinality_threshold,
                      number_of_histogram_bins, csv_columns_for_features,
                      number_of_histogram_bins, how_many_bags, bag_overlap_fraction, debug1''') 
        allowed_keys = 'training_datafile','entropy_threshold','max_depth_desired','csv_class_column_index',\
                       'symbolic_to_numeric_cardinality_threshold','csv_columns_for_features',\
                       'number_of_histogram_bins', 'how_many_bags','bag_overlap_fraction','debug1'
        keywords_used = kwargs.keys()
        for keyword in keywords_used:
            if keyword not in allowed_keys:
                raise ValueError(keyword + ":  Wrong keyword used --- check spelling") 
        training_datafile=entropy_threshold=max_depth_desired=csv_class_column_index=number_of_histogram_bins= None
        symbolic_to_numeric_cardinality_threshold=csv_columns_for_features=how_many_bags= None
        bag_overlap_fraction=debug1=None
        if kwargs and not args:
            if 'how_many_bags' in kwargs : how_many_bags = kwargs.pop('how_many_bags')
            if 'bag_overlap_fraction' in kwargs : bag_overlap_fraction = kwargs.pop('bag_overlap_fraction')
            if 'training_datafile' in kwargs : training_datafile = kwargs['training_datafile']
            if 'csv_class_column_index' in kwargs: csv_class_column_index = kwargs.pop('csv_class_column_index')
            if 'csv_columns_for_features' in kwargs: \
                                  csv_columns_for_features = kwargs.pop('csv_columns_for_features')
            if 'debug1' in kwargs  :  debug1 = kwargs.pop('debug1')
        if not args and training_datafile:
            self._training_datafile = training_datafile
        elif not args and not training_datafile:
                raise ValueError('''You must specify a training datafile''')
        else:
            if args[0] != 'evalmode':
                raise ValueError("""When supplying non-keyword arg, it can only be 'evalmode'""")
        if csv_class_column_index:
            self._csv_class_column_index        =      csv_class_column_index
        else:
            self._csv_class_column_index        =      None
        if csv_columns_for_features:
            self._csv_columns_for_features      =      csv_columns_for_features
        else: 
            self._csv_columns_for_features      =      None            
        self._number_of_training_samples        =      None
        self._how_many_bags                     =      how_many_bags
        self._segmented_training_data           =      {}
        self._all_trees                         =      {i:DecisionTree(**kwargs) for i in range(how_many_bags)}
        self._root_nodes                        =      []
        self._classifications                   =      None
        if bag_overlap_fraction is not None: 
            self._bag_overlap_fraction          =      bag_overlap_fraction 
        else:
            self._bag_overlap_fraction          =      0.20            
        self._bag_sizes                         =      []
        if debug1:
            self._debug1                        =      debug1
        else:
            self._debug1                        =      0


    def get_training_data_for_bagging(self):
        class_name_in_column = self._csv_class_column_index - 1  # subtract 1 because first col has record labels
        if not self._training_datafile.endswith('.csv'): 
            sys.exit("Aborted. get_training_data_from_csv() is only for CSV files")
        all_data = [line.rstrip().split(',') for line in open(self._training_datafile,"rU")]
        data_dict = {line[0] : line[1:] for line in all_data}
        self._number_of_training_samples = len(data_dict) - 1
        if '""' not in data_dict:
            sys.exit('''Aborted. The first row of CSV file must begin with "", must have a header '''
                     '''for the column that bears of the name of the class for each sample and the '''
                     '''headers for the columns have feature values in them''')
        feature_names = [item.strip('"') for item in data_dict['""']]
        class_column_heading = feature_names[class_name_in_column]
        feature_names = [feature_names[i-1] for i in self._csv_columns_for_features]
        class_for_sample_dict = { "sample_" + key.strip('"') : 
               class_column_heading + "=" + data_dict[key][class_name_in_column] 
                                                   for key in data_dict if key != '""'}
        sample_names = ["sample_" + key for key in data_dict if key != '""']
        random.shuffle(sample_names)
        bag_size = int(len(sample_names) / self._how_many_bags)      
        def bags(l,n):
            for i in range(0,len(l),n):
                yield l[i:i+n]
        data_sample_bags = list(bags(sample_names, bag_size))[0:self._how_many_bags]
        if (len(sample_names) %  bag_size) > 0:
            data_sample_bags[-1] += sample_names[ self._how_many_bags * bag_size : ]
        self._bag_sizes = [ len(data_sample_bags[i]) for i in range(self._how_many_bags) ]
        if self._bag_overlap_fraction is not None:
            number_of_samples_needed_from_other_bags = int( len(data_sample_bags[0]) * self._bag_overlap_fraction )
            for i in range(self._how_many_bags): 
                samples_in_other_bags = reduce( lambda x,y: x+y, [data_sample_bags[x]
                                                                  for x in range(self._how_many_bags) if x != i])
                new_samples_to_be_added = random.sample(samples_in_other_bags, number_of_samples_needed_from_other_bags)
                data_sample_bags[i] += new_samples_to_be_added
            self._bag_sizes = [ len(data_sample_bags[i]) for i in range(self._how_many_bags) ]
        class_for_sample_dict_bags = { i : {sample_name :  class_for_sample_dict[sample_name]
                                 for sample_name in data_sample_bags[i] } for i in range(self._how_many_bags) }
        feature_values_for_samples_dict = {"sample_" + key.strip('"') : 
              list(map(operator.add, list(map(operator.add, feature_names, "=" * len(feature_names))), 
           [str(convert(data_dict[key][i-1].strip('"'))) for i in self._csv_columns_for_features])) 
                                                               for key in data_dict if key != '""'}
        feature_values_for_samples_dict_bags =  { i : {sample_name :  feature_values_for_samples_dict[sample_name]
                                 for sample_name in data_sample_bags[i] } for i in range(self._how_many_bags) }
        features_and_values_dict = {data_dict['""'][i-1].strip('"') : 
                      [convert(data_dict[key][i-1].strip('"')) for key in data_dict if key != '""']  
                            for i in self._csv_columns_for_features} 
        features_and_values_dict_bags = { j :  { data_dict['""'][i-1].strip('"') :
          [convert(data_dict[key][i-1].strip('"')) for  key in data_dict
                                                   if "sample_" + key in data_sample_bags[j] ]
                            for i in self._csv_columns_for_features } for j in range(self._how_many_bags) }
        all_class_names = sorted(list(set(class_for_sample_dict.values())))
        numeric_features_valuerange_dict_bags = {i : {} for i in range(self._how_many_bags)}        
        feature_values_how_many_uniques_dict_bags = {i : {} for i in range(self._how_many_bags)}
        features_and_unique_values_dict_bags = {i : {} for i in range(self._how_many_bags)}
        for i in range(self._how_many_bags):
            for feature in features_and_values_dict_bags[i]:
                unique_values_for_feature = list(set(features_and_values_dict_bags[i][feature]))
                unique_values_for_feature = sorted(list(filter(lambda x: x != 'NA', unique_values_for_feature)))
                feature_values_how_many_uniques_dict_bags[i][feature] = len(unique_values_for_feature)
                if all(isinstance(x,float) for x in unique_values_for_feature):
                    numeric_features_valuerange_dict_bags[i][feature] = \
                                  [min(unique_values_for_feature), max(unique_values_for_feature)]
                    unique_values_for_feature.sort(key=float)
                features_and_unique_values_dict_bags[i][feature] = sorted(unique_values_for_feature)
        for i in range(self._how_many_bags):                
            self._all_trees[i]._class_names = all_class_names
            self._all_trees[i]._feature_names = feature_names
            self._all_trees[i]._samples_class_label_dict = class_for_sample_dict_bags[i]
            self._all_trees[i]._training_data_dict  =  feature_values_for_samples_dict_bags[i]
            self._all_trees[i]._features_and_values_dict    =  features_and_values_dict_bags[i]
            self._all_trees[i]._features_and_unique_values_dict    =  features_and_unique_values_dict_bags[i]
            self._all_trees[i]._numeric_features_valuerange_dict = numeric_features_valuerange_dict_bags[i]
            self._all_trees[i]._feature_values_how_many_uniques_dict = feature_values_how_many_uniques_dict_bags[i]
        if self._debug1:
            for i in range(self._how_many_bags):            
                print("\n\n=============================   For bag %d   ==================================\n" % i)
                print("\nAll class names: " + str(self._all_trees[i]._class_names))
                print("\nEach sample data record:")
                for item in sorted(self._all_trees[i]._training_data_dict.items(), key = lambda x: sample_index(x[0]) ):
                    print(item[0]  + "  =>  "  + str(item[1]))
                print("\nclass label for each data sample:")
                for item in sorted(self._all_trees[i]._samples_class_label_dict.items(), key=lambda x: sample_index(x[0])):
                    print(item[0]  + "  =>  "  + str(item[1]))
                print("\nfeatures and the values taken by them:")
                for item in sorted(self._all_trees[i]._features_and_values_dict.items()):
                    print(item[0]  + "  =>  "  + str(item[1]))
                print("\nnumeric features and their ranges:")
                for item in sorted(self._all_trees[i]._numeric_features_valuerange_dict.items()):
                    print(item[0]  + "  =>  "  + str(item[1]))

                print("\nnumber of unique values in each feature:")
                for item in sorted(self._all_trees[i]._feature_values_how_many_uniques_dict.items()):
                    print(item[0]  + "  =>  "  + str(item[1]))

    def get_number_of_training_samples(self):
        return self._number_of_training_samples

    def show_training_data_in_bags(self):
        for i in range(self._how_many_bags):
            print("\n\n=============================   For bag %d   ==================================\n" % i)
            self._all_trees[i].show_training_data()            

    def calculate_first_order_probabilities(self):            
        list(map(lambda x: self._all_trees[x].calculate_first_order_probabilities(), range(self._how_many_bags)))

    def calculate_class_priors(self):            
        list(map(lambda x: self._all_trees[x].calculate_class_priors(), range(self._how_many_bags)))
        
    def construct_decision_trees_for_bags(self):            
        self._root_nodes = \
             list(map(lambda x: self._all_trees[x].construct_decision_tree_classifier(), range(self._how_many_bags)))

    def display_decision_trees_for_bags(self):
        for i in range(self._how_many_bags):
            print("\n\n=============================   For bag %d   ==================================\n" % i)
            self._root_nodes[i].display_decision_tree("     ")

    def classify_with_bagging(self, test_sample):
        self._classifications = list(map(lambda x: self._all_trees[x].classify(self._root_nodes[x], test_sample),
                                   range(self._how_many_bags)))

    def display_classification_results_for_each_bag(self):         
        classifications = self._classifications
        if classifications is None:
            raise AttributeError('''You must first call "classify_with_bagging()" before invoking 
                                "display_classification_results_for_each_bag()" ''')
        solution_paths = list(map(lambda x: x['solution_path'], classifications))
        for i in range(self._how_many_bags):
            print("\n\n=============================   For bag %d   ==================================\n" % i)
            print("\nbag size: %d\n" % self._bag_sizes[i])
            classification = classifications[i]
            del classification['solution_path']
            which_classes = list( classification.keys() )
            which_classes = sorted(which_classes, key=lambda x: classification[x], reverse=True)
            print("\nClassification:\n")
            print("     "  + str.ljust("class name", 30) + "probability")
            print("     ----------                    -----------")
            for which_class in which_classes:
                if which_class is not 'solution_path':
                    print("     "  + str.ljust(which_class, 30) +  str(classification[which_class]))
            print("\nSolution path in the decision tree: " + str(solution_paths[i]))
            print("\nNumber of nodes created: " + str(self._root_nodes[i].how_many_nodes()))

    def get_majority_vote_classification(self):
        classifications = self._classifications
        if classifications is None:
            raise AttributeError('''You must first call "classify_with_bagging()" before invoking 
                                "display_classification_results_for_each_bag()" ''')
        decision_classes = {class_label : 0 for class_label in self._all_trees[0]._class_names}
        for i in range(self._how_many_bags):
            classification = classifications[i]
            if 'solution_path' in classification:
                del classification['solution_path']
            sorted_classes = sorted(list(classification.keys()), key=lambda x: classification[x], reverse=True)  
            decision_classes[sorted_classes[0]] += 1
        sorted_by_votes_decision_classes = \
                         sorted(list(decision_classes.keys()), key=lambda x: decision_classes[x], reverse=True)
        return sorted_by_votes_decision_classes[0]

    def get_all_class_names(self):
        return self._all_trees[0]._class_names
