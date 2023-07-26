const data = {
  id: "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  name: "My new project",
  description: "My new project description",
  thumbnail_url: "https://assets.plan4better.de/api/thumbnail/1.png",
  tags: ["tag1", "tag2"],
  created_by: "elias.pajares@plan4better.de",
  updated_by: "elias.pajares@plan4better.de",
  created_at: "2021-03-03T09:00:00.000000Z",
  updated_at: "2021-03-03T09:00:00.000000Z",
  shared_with: [
    {
      group_id: 1,
      group_name: "My Group 1",
      image_url: "https://assets.plan4better.de/api/thumbnail/1.png",
    },
    {
      group_id: 2,
      group_name: "My Group 2",
      image_url: "https://assets.plan4better.de/api/thumbnail/2.png",
    },
  ],
  scale_show: false,
  navigation_control: false,
  MAP_ACCESS_TOKEN:
    "pk.eyJ1IjoiZWxpYXNwYWphcmVzIiwiYSI6ImNqOW1scnVyOTRxcWwzMm5yYWhta2N2cXcifQ.aDCgidtC9cjf_O75frn9lA",
  map_style: "mapbox://styles/mapbox/streets-v11",
  initial_view_state: {
    latitude: 48.1502132,
    longitude: 11.5696284,
    zoom: 10,
    min_zoom: 0,
    max_zoom: 20,
    bearing: 0,
    pitch: 0,
  },
  reports: [],
  layers: [
    {
      id: "123e4567-e89b-12d3-a456-426614174000",
      name: "Edge Layer",
      group: "Example Group 1",
      description: "This is an example for a streets layer (line)",
      type: "tile_layer",
      created_at: "2023-07-11T00:00:00",
      created_by: "example_user",
      updated_at: "2023-07-11T00:00:00",
      updated_by: "example_user",
      active: "True",
      data_source_name: "Example Data Source",
      data_reference_year: 2020,
      url: "https://api.mapbox.com/v4/eliaspajares.cljxyjs6x02672oqimtbmde3u-92yjl/{z}/{x}/{y}.mvt?access_token=pk.eyJ1IjoiZWxpYXNwYWphcmVzIiwiYSI6ImNqOW1scnVyOTRxcWwzMm5yYWhta2N2cXcifQ.aDCgidtC9cjf_O75frn9lA",
      style:
        "https://api.mapbox.com/styles/v1/eliaspajares/cljxzoemb003y01qr59fx3mpq?access_token=pk.eyJ1IjoiZWxpYXNwYWphcmVzIiwiYSI6ImNqOW1scnVyOTRxcWwzMm5yYWhta2N2cXcifQ.aDCgidtC9cjf_O75frn9lA",
      data_type: "mvt",
    },
    {
      id: "123e4567-e89b-12d3-a456-426614174001",
      name: "POI Layer",
      group: "Opportunities",
      description: "This is an example for a point layer (point of interests)",
      type: "tile_layer",
      created_at: "2023-07-11T00:00:00",
      created_by: "example_user",
      updated_at: "2023-07-11T00:00:00",
      updated_by: "example_user",
      active: "True",
      data_source_name: "Example Data Source",
      data_reference_year: 2020,
      url: "https://api.mapbox.com/v4/eliaspajares.cljxyaynj02532aqi9rh1kz0g-77qff/{z}/{x}/{y}.mvt?access_token=pk.eyJ1IjoiZWxpYXNwYWphcmVzIiwiYSI6ImNqOW1scnVyOTRxcWwzMm5yYWhta2N2cXcifQ.aDCgidtC9cjf_O75frn9lA",
      style:
        "https://api.mapbox.com/styles/v1/eliaspajares/cljxz3bl1003v01qy7k5m0apj?access_token=pk.eyJ1IjoiZWxpYXNwYWphcmVzIiwiYSI6ImNqOW1scnVyOTRxcWwzMm5yYWhta2N2cXcifQ.aDCgidtC9cjf_O75frn9lA",
      data_type: "mvt",
    },
    {
      id: "123e4567-e89b-12d3-a456-426614174002",
      name: "AOI Layer",
      group: "Opportunities",
      description: "This is an example for a areas of interest layer (polygon)",
      type: "tile_layer",
      created_at: "2023-07-11T00:00:00",
      created_by: "example_user",
      updated_at: "2023-07-11T00:00:00",
      updated_by: "example_user",
      active: "False",
      data_source_name: "Example Data Source",
      data_reference_year: 2021,
      url: "https://api.mapbox.com/v4/eliaspajares.cljxc2rek01ow2alyl0cy0y2j-63c9z/{z}/{x}/{y}.mvt?access_token=pk.eyJ1IjoiZWxpYXNwYWphcmVzIiwiYSI6ImNqOW1scnVyOTRxcWwzMm5yYWhta2N2cXcifQ.aDCgidtC9cjf_O75frn9lA",
      style:
        "https://api.mapbox.com/styles/v1/eliaspajares/cljyel7yl005r01pfcd4h0epj?access_token=pk.eyJ1IjoiZWxpYXNwYWphcmVzIiwiYSI6ImNqOW1scnVyOTRxcWwzMm5yYWhta2N2cXcifQ.aDCgidtC9cjf_O75frn9lA",
      data_type: "mvt",
    },
    {
      id: "123e4567-e89b-12d3-a456-426614174003",
      name: "Example Image Layer",
      group: "Example Group 2",
      description: "This is an example for a image layer",
      type: "image_layer",
      created_at: "2023-07-11T00:00:00",
      created_by: "example_user",
      updated_at: "2023-07-11T00:00:00",
      updated_by: "example_user",
      active: "True",
      data_source_name: "Example Data Source",
      data_reference_year: 2020,
      url: "https://www.lfu.bayern.de/gdi/wms/laerm/hauptverkehrsstrassen?LAYERS=mroadbylden2022,mroadbyln2022",
      legend_urls: [
        "https://www.lfu.bayern.de/gdi/wms/laerm/hauptverkehrsstrassen?request=GetLegendGraphic&version=1.3.0&format=image/png&layer=mroadbyln&SERVICE=WMS&SLD_VERSION=1.1.0&STYLE=&TRANSPARENT=true",
        "https://www.lfu.bayern.de/gdi/wms/laerm/hauptverkehrsstrassen?request=GetLegendGraphic&version=1.3.0&format=image/png&layer=mroadbyln&SERVICE=WMS&SLD_VERSION=1.1.0&STYLE=&TRANSPARENT=true",
      ],
      data_type: "wms",
    },
    {
      id: "123e4567-e89b-12d3-a456-426614174004",
      name: "Example Image Layer XYZ",
      group: "Example Group 2",
      description: "This is an example for a image layer",
      type: "image_layer",
      created_at: "2023-07-11T00:00:00",
      created_by: "example_user",
      updated_at: "2023-07-11T00:00:00",
      updated_by: "example_user",
      active: "True",
      data_source_name: "Example Data Source",
      data_reference_year: 2020,
      url: "https://tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey=402ce1ca8eb54457bdf65e2b261c5132",
      data_type: "xyz",
    },
  ],
};

export default data;
