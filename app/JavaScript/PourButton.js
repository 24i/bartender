import React, { Component } from 'react';
import {
  StyleSheet,
  View,
} from 'react-native';

import{ CircleButton } from 'react-native-button-component';

export default class PourButton extends Component {
  constructor(props) {
    super(props);
    this.state = {
      pour: 'pour',
      pourProgress: 0,
    };

    this.pour = this.pour.bind(this);
  }

  pour() {
    this.setState({ pour: 'pouring', pourProgress: 0 });
    //TODO: Make pour call to bartender


    //TODO: Find the time it takes to pour a drink and  set it here to count correctly.
    //TODO: Maybe get the time data returned from server
    const intervalId = setInterval(() => {
      if (this.state.pourProgress < 100) {
        this.setState({ pourProgress: this.state.pourProgress + 1 });
      } else {
        clearInterval(intervalId);
        this.setState({ pour: 'pour'});
      }
    }, 50);
  }

  render() {
    return (
      <View style={styles.container}>
        <CircleButton
            shape="circle"
            states={{
              pour: {
                text: 'Pour',
                backgroundColors: ['#ff0000', '#ff0000'],
                onPress: this.pour,
                //NOTE: using spinned as progress animation was messed up
                spinner: false
              },
              pouring: {
                text: 'Pouring...',
                backgroundColors: ['#ff0000', '#ff0000'],
                //NOTE: using spinned as progress animation was messed up
                spinner: true
              },
            }}
            buttonState={this.state.pour}
          />
        </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: 0,
    justifyContent: 'center',
    alignItems: 'center',
  }
});
