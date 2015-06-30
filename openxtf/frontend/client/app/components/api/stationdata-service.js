/**
 * @fileoverview A service which fetches data for a station.
 */

var proto = require('openxtf-proto').openxtf;

/**
 * A service which tracks StationData objects which fetch and store data about
 * stations.
 * @constructor
 */
function StationDataService($http, $log, $q, $cacheFactory) {
  this.$http = $http;
  this.$log = $log;
  this.$q = $q;
  this.stations = $cacheFactory('STATION_DATA_CACHE', { capacity: 20 });
}
module.exports = StationDataService;

/**
 * @param {string} stationName
 * @return {StationData} Returns a station data object for this station.
 */
StationDataService.prototype.getStationData = function(stationName) {
  var cached = this.stations.get(stationName);
  if (!cached) {
    cached = this.stations.put(
        stationName,
        new StationData(this.$http, this.$log, this.$q, stationName));
  }
  return cached;
};


/**
 * A station data object which unwraps a promise for station data.
 *
 * It should be used to access the data for a given station.  This helps prevent
 * duplicate fetching and centralizes who fetches and stores a copy of station
 * data.
 * @constructor
 */
function StationData($http, $log, $q, stationName) {
  this.$http = $http;
  this.$log = $log;
  this.$q = $q;
  this.stationName = stationName;

  this.fetchRequest = null;
  this.stationData = null;
  this.updateData();
}

/** @return {?XTFStationResponse} A nullable station response. */
StationData.prototype.getData = function() {
  return this.stationData;
};

/** Updates the stored station data. */
StationData.prototype.updateData = function() {
  if (this.fetchRequest) {
    return this.fetchRequest;
  }
  this.fetchRequest = this.$http.get('/api/stations/' + this.stationName, {
    responseType: 'arraybuffer'
  }).then(this.onSuccess.bind(this), this.onFailure.bind(this));
  return this.fetchRequest;
};


/** Transforms the response into a station response protobuf. */
StationData.prototype.onSuccess = function(response) {
  if (!response.data) {
    this.$log.warn('No data for station', this.stationName);
    return this.$q.reject('no data');
  }
  this.stationData = proto.XTFStationResponse.decode(response.data);
  this.fetchRequest = null;
  return this.stationData;
};

/** Deals with station fetch failure. */
StationData.prototype.onFailure = function(err) {
  this.$log.warn('Failed to fetch station', this.stationName);
  return this.$q.reject(err.data);
};
