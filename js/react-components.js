'use strict';

const e = React.createElement;

class SongTableRow extends React.Component {
  render() {
    return(
      e('tr', {},
        e('td', {}, this.props.record.artist),
        e('td', {},
          e('a', {href: this.props.record.link}, this.props.record.title)
        )
      )
    );
  }
}

class SongTable extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    var tableRows = this.props.songs.map(function(record, index) {
      return e(SongTableRow, {key: index, record: record});
    });

    return(
      e('table', {className: 'song-table'},
        e('thead', {},
          e('tr', {},
            e('th', {}, 'Artist'),
            e('th', {}, 'Title')
          )
        ),
        e('tbody', {},
          tableRows
        )
      )
    );
  }
}
