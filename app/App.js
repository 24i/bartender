import React, { Component } from 'react';
import { View, StyleSheet } from 'react-native';
import PourButton from './JavaScript/PourButton'
import DrinkSelector from './JavaScript/DrinkSelector'
import Icon from 'react-native-ionicons'

class App extends Component {

  //TODO: Icon package i've used doensnt support touch listeners,
  //TODO: the actual react-native icons package messes up with something RE bable. Investigate.
  render() {

    return (
      <View style={styles.container}>

        <View style={styles.header}>
          <View style={{
              flex: 1,
              justifyContent: 'flex-start',
              }}>
              <Icon ios="ios-cloud-outline" android="md-cloud-outline" color="#ff0000" size={40}/>
            </View>

          <View style={{
            flex: 1,
            flexDirection: 'row',
            justifyContent: 'flex-end',
            }}>
            <Icon ios="ios-settings" android="md-settings" color="#ff0000" size={40}/>
          </View>
        </View>

        <View style={styles.contentContainer}>
          <DrinkSelector></DrinkSelector>
        </View>

        <View style={styles.footer}>
          <View style={{
            flex: 1,
            flexDirection: 'row',
            justifyContent: 'center',
            }}>
            <PourButton></PourButton>
          </View>
        </View>

      </View>
    );
  }
}

var styles = StyleSheet.create({
  title: {

  },
  slide: {

  },
  container: {
      flex: 1,
      backgroundColor: '#1a1917',
  },
  titleWrapper: {

  },
  inputWrapper: {

  },
  header: {
    flexDirection: 'row',
    flex: 0.5, // pushes the footer to the end of the screen
    margin: 8
  },
  contentContainer: {
      flex: 1.5 // pushes the footer to the end of the screen
  },
  footer: {
      backgroundColor: '#1a1917',
      height: 100,
      margin: 12
  }
});

export default App;
