import React from 'react';
import logo from './logo.svg';
import './App.css';

const LEVEL_NAMES = {
  1: "初級",
  2: "中級",
  3: "上級",
}

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      content: null,
      loading: true,
    }
  }

  async componentDidMount() {
    const payload = {
      'method': 'GET',
      'mode': 'cors',
    }
    const response = await fetch('https://cmn9d65493.execute-api.ap-northeast-1.amazonaws.com/production', payload)
    if (response.ok) {
      const content = await response.json()
      this.setState({content: content, loading: false})
    }
    else {
      this.setState({loading: false})
    }
  }

  render() {
    if (this.state.loading) {
      return (<div className="App">Loading...</div>)
    }
    if (!this.state.content) {
      return (<div className="App">Error: Should be try to reload content.</div>)
    }

    let content = []
    for (const day of this.state.content) {
      let times = []
      for (const time of day['times']) {
        times.push(
          <div className="time">{day['date']} {time['time']}: {time['qty']}人 ({LEVEL_NAMES[time['level']]})</div>
        )
      }
      content.push(
        <div className="day">{times}</div>
      )
    }
    return (
      <div className="App">
        {content}
      </div>
    );
  }
}

export default App;
