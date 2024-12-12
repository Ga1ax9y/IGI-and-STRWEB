import React, { Component } from 'react';

class TimeDisplay extends Component {

  press = () =>{
    console.log(this);
    alert("Hello from class-component!")
  }
  print(name, age){
    alert(`Name ${name}, Age: ${age}`);
}


  render() {
    const { label, time } = this.props;

    return (
      <div className="time-display">
        <h3 onClick={this.press}>{label}</h3>
        <p onClick={() => this.print("Tom", 36)}>{time}</p>
      </div>
    );
  }
}

export default TimeDisplay;
