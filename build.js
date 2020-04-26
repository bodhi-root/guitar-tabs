var Metalsmith    = require('metalsmith');
var markdown      = require('metalsmith-markdown');
var layouts       = require('metalsmith-layouts');
var permalinks    = require('metalsmith-permalinks');
var writemetadata = require('metalsmith-writemetadata');
var assets        = require('metalsmith-assets');

validateTabs = function() {
  return function(files, metalsmith, done) {
    setImmediate(done);
    Object.keys(files).forEach(function(file) {

      var data = files[file];
      var keys = Object.keys(data);

      if (keys.indexOf("title") < 0) {
        console.log("WARNING: " + file + " missing property 'title'");
      }
      if (keys.indexOf("artist") < 0) {
        console.log("WARNING: " + file + " missing property 'artist'");
      }
    });
  };
}

/**
 * Generates an index file with a list of all songs.
 * TODO: this should be fancier (like a table)
 # Could also include song ratings, tunings, and easy ratings
 */
writeIndex = function() {
  return function(files, metalsmith, done) {
    setImmediate(done);

    var songData = [];
    Object.keys(files).forEach(function(file) {
      var data = files[file];
      var info = {
        title: data.title,
        artist: data.artist,
        link: file,
        tuning: data.tuning,
        rating: data.rating,
        difficulty: data.difficulty
      };
      songData.push(info);
    });

    files["index.html"] = {
      title: "Song Index",
      layout: "song_index.html",
      songData: JSON.stringify(songData),
      contents: Buffer.from("This page does not have content")
    }

  }
}

/**
 * Removes files that shouldn't be here
 */
removeFiles = function(file_names) {
  return function(files, metalsmith, done) {
    setImmediate(done);
    Object.keys(files).forEach(function(file) {
      if (file_names.indexOf(file) >= 0) {
        delete files[file];
      }
    });
  }
}

/**
 * Remove spaces in file names, replacing them with dashes instead
 */
removeSpaces = function() {
  return function(files, metalsmith, done) {
    setImmediate(done);
    Object.keys(files).forEach(function(file) {
      new_file_name = file.replace(/ /g, "-");
      if (file !== new_file_name) {
        files[new_file_name] = files[file];
        delete files[file];
      }
    });
  }
}

Metalsmith(__dirname)
  .metadata({
    siteTitle: "Dan's Guitar Tabs"
  })
  .source('./src')
  .destination('./build')
  .clean(true)
  .use(removeFiles(["songs\\_template.md"]))
  .use(removeSpaces())
  .use(validateTabs())
  .use(markdown())
  .use(writeIndex())
  .use(layouts({
    engine: 'handlebars',
    default: 'song.html'
  }))
  .use(writemetadata({    // write the JS object for each file into .json
    pattern: ['**/*'],
    ignorekeys: ['next', 'previous'],
    bufferencoding: 'utf8'
  }))
  .use(assets({
    source: './public',
    destination: '.'
  }))
  .build(function(err, files) {
    if (err) { throw err; }
  });
