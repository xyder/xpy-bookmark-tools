(function (AppController, $, undefined){
    var self = AppController;

    /***
     * Performs an ajax call to the specified uri with the given method and data
     * @param uri path to be used in the ajax call
     * @param method http method to be used
     * @param data object to be converted to json and sent attached to the request
     * @returns the return value from the jquery ajax call
     */
    self.ajax = function (uri, method, data) {
        var ajax_params = {
            url: uri,
            type: method ? method : 'GET',
            accepts: 'application/json',
            cache: false,
            dataType: 'json',
            data: method === 'GET' ? data : JSON.stringify(data),
            timeout: 1000,
            complete: function(jqXHR){
                switch(jqXHR.status){
                    case 0:
                        // no response
                        break;
                    case 200:
                        // success
                        break;
                    case 400:
                        // bad request
                        console.log('Ajax error: Bad request.');
                        break;
                    case 403:
                        // not authorized
                        break;
                    case 404:
                        // not found
                        break;
                    default:
                        //other status codes
                        console.log('Ajax call returned error: ' + jqXHR.status)
                }
            }
        };

        // filter DELETE methods out because they can't have application/json content-type
        if (method !== 'DELETE'){
            ajax_params['contentType'] = 'application/json';
        }
        return $.ajax(ajax_params);
    };
}(window.AppController = window.AppController || {}, jQuery));
