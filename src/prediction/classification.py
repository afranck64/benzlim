from sklearn import tree
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from  .db import StationDAO



STDEV_STEP = 2             #10
AVG_PRICE_STEP = 10         #50
UPDATE_INTERVAL_STEP = 90  #900
DAILY_UPDATE_STEP = 1       #2

CATEGORIES = dict()

def get_group(extended_station_infos, daily_update_step=DAILY_UPDATE_STEP,
              stdev_step=STDEV_STEP, avg_price_step=AVG_PRICE_STEP,
              update_interval_step=UPDATE_INTERVAL_STEP):
    daily_updates, update_interval, avg_price, stedv = extended_station_infos[-4:]
    daily_updates = daily_updates - (daily_updates - 1) % daily_update_step + 1
    #update_interval = update_interval - (update_interval -1) % update_interval_step + 1
    avg_price = avg_price - (avg_price -1) % avg_price_step + 1
    stedv = stedv - (stedv - 1) % stdev_step + 1

    group = hash((avg_price, daily_updates, stedv, ))
    cat = CATEGORIES.get(group, [])
    cat.append(extended_station_infos[0])
    CATEGORIES[group] = cat
    return group

def get_features_extended_station_dep(ext_station_row):
    #sr = ext_station_row
    #return sr[0], sr[1].lower(), sr[2].lower(), sr[3].lower(), sr[4], sr[5], sr[6].lower()  #TODO should be done in the DB
    pass

def get_station_features(station_row):
    sr = station_row
    #return sr[1].lower(), sr[2].lower(), sr[3].lower(), sr[4], sr[5], sr[6].lower(), sr[7], sr[9]  #TODO should be done in the DB
    return sr[5], sr[7], sr[8]

def get_prepared_data(ext_stations, discard_dirty=True):
    """return features with corresponding classes,
    discard items with missing information, such as prices not available if discard_dirty is True"""
    EXT_PRICE_ID = -2
    if discard_dirty:
        ext_stations = tuple(ext_station for ext_station in ext_stations if ext_station[EXT_PRICE_ID]>0)
        print len(ext_stations)
    features = (get_station_features(row) for row in ext_stations)
    classes = (get_group(row) for row in ext_stations)
    
    return features, classes


def train(features, classes):
    clf = tree.DecisionTreeClassifier()
    features = tuple(features)
    classes = tuple(classes)
    #ohe = OneHotEncoder(categorical_features=[1,2,3,6])     #[1,2,3,6]
    #X = ohe.fit_transform(features)
    #le_1 = LabelEncoder()
    #le_2 = LabelEncoder()
    #le_3 = LabelEncoder()
    #le_6 = LabelEncoder()
    #le_1 = le_1.fit(tuple(row[1] for row in features))
    #le_2 = le_2.fit(tuple(row[2] for row in features))
    #le_3 = le_3.fit(tuple(row[3] for row in features))
    #le_6 = le_6.fit(tuple(row[6] for row in features))
    print features[0], classes[0]
    #X = ohe.fit_transform(features).toarray()
    X = features
    Y = classes
    clf = clf.fit(X, Y)
    return clf



if __name__ == "__main__":
    stations = StationDAO.getAll()
    """
    for station in stations:
        get_group(station)
    siz_cat = len(CATEGORIES)
    siz_tot = len(stations)
    percent = siz_cat*1.0 / siz_tot
    print siz_cat, siz_tot, percent
    """
    clf = train(*get_prepared_data(stations))
    TEST_STATION_ID = 7
    station = StationDAO.get(TEST_STATION_ID)
    print get_station_features(station), get_group(station), clf.predict(get_station_features(station))
    print "PROBAS", max(clf.predict_proba(get_station_features(station)))
    print "ALL CATS: ", len(CATEGORIES), len([item for item in CATEGORIES.values() if len(item)>=250])
    print CATEGORIES[int(clf.predict(get_station_features(station)))]

    #for ex_station in stations[:10]:
    #    print ex_station, get_group(ex_station), clf.predict(get_station_features(ex_station))