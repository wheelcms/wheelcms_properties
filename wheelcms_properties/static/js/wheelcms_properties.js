wheelcms_properties = angular.module('wheelcms_properties', ["schemaForm", "ui.sortable"]);

wheelcms_properties.factory('FormTool', function($sce) {
    var trust = $sce.trustAsHtml;
     // trust = function(s) { return s; };

    return {
        to_schema: function(e) {
            var s = {
                type: "object",
                properties: {}
            };
            var ee = {type: e.type, title: e.title};

            if(typeof e.choices != "undefined") {
                ee['enum'] = e.choices;
            }

            if(e.type == "number") {
                ee['default'] = parseInt(e.default_value, 10);
            }
            else if(e.type == "checkboxes") {
                ee['default'] = e.default_value.split("\n");
            }
            else {
                ee['default'] = e.default_value;
            }
            s.properties[e.id] = ee;

            return s;
        },

        to_form: function(e) {
            var field = {};

            field.key = e.id; // trust(e.id);
            field.type = (e.input || "text");

            if(e.choices) {
                field.titleMap = [];
                for(var c = 0; c < e.choices.length; c++) {
                    var cc = trust(e.choices[c]);
                    field.titleMap.push({value:e.choices[c], name:cc});
                }
            }

            return [ field ];
        },
        build_schemaform: function(formdef) {
            var schema = { type: "object", properties: {} };

            var form = [];

            for(var idx = 0; idx < formdef.length; idx++) {
                var e = formdef[idx];
                var s = this.to_schema(e);
                var f = this.to_form(e);

                schema.properties[e.id] = s.properties[e.id];
                form.push(f[0]);
            }
            return {schema: schema, form: form};
        }
    }
});

wheelcms_properties.controller("BaseFieldsEditCtrl", function($scope, $http, $modal, $filter, FormTool, Notifier) {
    $scope.changed = false;
    $scope.field_def = [];
    $scope.base = "";

    $scope.initialize = function(base) {
        $scope.base = base;

        $http.get(base).then(function(result) {
            $scope.field_def = result.data.form;
            $scope.extra = result.data.extra;
            console.log("extra", $scope.extra);
            build_schemaforms();
        });

        $scope.model = {};
    };

    $scope.sortableOptions = {
        update: function(e, ui) {
            $scope.changed = true;
        }
    };

    var build_schemaforms = function() {
        $scope.schemaforms = [];
        for(var idx = 0; idx < $scope.field_def.length; idx++) {
            var e = $scope.field_def[idx];
            $scope.schemaforms.push({schema: FormTool.to_schema(e), form: FormTool.to_form(e),
                                     field: e, model: {}});
        }
    }

    build_schemaforms();


    $scope.newEditField = function(field) {
        var m = $modal.open({
                        templateUrl: 'AddEditField.html',
                        controller: 'AddEditFieldCtrl',
                        resolve: {
                            field: function() {
                                if(field !== null) {
                                    return field.field;
                                }
                            }
                        }
                });
        m.result.then(function(result) {
            if(field === null) {
                // add
                $scope.field_def.push(result);
                $scope.schemaforms.push({schema: FormTool.to_schema(result),
                                         form: FormTool.to_form(result),
                                         field: result,
                                         model: {}});
            }
            else {
                // update
                field.field = result;
                field.schema = FormTool.to_schema(result);
                field.form = FormTool.to_form(result);
                field.model = {};
            }

            $scope.changed = true;
        });
    };

    $scope.save = function() {
        var reordered = [];
        for(var idx = 0; idx < $scope.schemaforms.length; idx++) {
            reordered.push($scope.schemaforms[idx].field);
        }
        console.log("POST", $scope.extra);
        $http.post($scope.base,
                   {
                        data: $filter('json')(reordered),
                        extra: $filter('json')($scope.extra || {})
                   }).then(function(result) {
                             $scope.field_def = result.data.form;
                             $scope.extra = result.data.extra;
                             build_schemaforms();
                             $scope.changed = false;
                             Notifier.notify("info", "Saved");
        });
    }
});


wheelcms_properties.controller("WheelPropertiesCtrl",
                               function($scope, $controller, $rootScope,
                                        $http, FormTool) {
    $scope.state = "list";
    $scope.forms = [];

    var baseurl = $rootScope.urlbase + '?config=spoke_properties';

    var refreshforms = function() {
        $http.get(baseurl + "&action=formlist").then(function(result) {
            $scope.forms = result.data;
            console.log($scope.forms);
        });
    }

    refreshforms();

    $controller('BaseFieldsEditCtrl', {$scope:$scope});

    /*
     * We need to save additional data on top of the base form:
     * - name for the form
     * - content types it's bound to
     * Either hook into the BaseFieldsEditCtrl edit/delete, or do a second get/post
     */
    $scope.newEditForm = function(id) {
        $scope.state = "edit";
        $scope.extra = {};

        var url = baseurl + '&action=formdata';
        if(id !== null) {
            url += "&id=" + id;
        }
        $scope.initialize(url);
    };
    $scope.saveForm = function(id) {
        console.log("Saving extra", $scope.extra);
        $scope.save(); // defined in base controller
        $scope.state = "list";
        refreshforms();
    };
});

wheelcms_properties.controller('AddEditFieldCtrl', function($scope, $modalInstance, field) {
    $scope.fielddata = angular.copy(field || {});

    $scope.data_types = [
            {title:"String", value:'string'},
            {title:"Number", value:'number'},
            {title:"Multiple", value:'checkboxes'}
        ];

    $scope.input_types = [
            {title:"Input", value:"text"},
            {title:"Password", value:"password"},
            {title:"Text area", value: "textarea"},
            {title:"Number", value: "number"},
            {title:"Checkbox", value: "checkbox"},
            {title:"Checkboxes", value: "checkboxes"},
            {title:"Select", value: "select"}
    ];

    for(var i = 0; i < $scope.data_types.length; i++) {
        if($scope.data_types[i].value == $scope.fielddata.type) {
            $scope.fielddata._type = $scope.data_types[i];
        }
    }
    for(var i = 0; i < $scope.input_types.length; i++) {
        if($scope.input_types[i].value == $scope.fielddata.input) {
            $scope.fielddata._input = $scope.input_types[i];
        }
    }

    if($scope.fielddata.choices) {
        $scope.fielddata._choices = $scope.fielddata.choices.join("\n")
    }

    $scope.ok = function () {
        // convert field/data selection back
        $scope.fielddata.type = $scope.fielddata._type.value || 'string';
        $scope.fielddata.input = $scope.fielddata._input.value || 'text';
        if($scope.fielddata._choices) {
            var choices = $scope.fielddata._choices.split("\n");
            $scope.fielddata.choices = [];
            for(var c = 0; c < choices.length; c++) {
                $scope.fielddata.choices.push(choices[c]);
            }
            if($scope.fielddata.choices.length == 0) {
                delete $scope.fielddata.choices;
            }
        }
        else {
            delete $scope.fielddata.choices;
        }
        $modalInstance.close($scope.fielddata);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});

