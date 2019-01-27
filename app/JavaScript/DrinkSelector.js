import React, { Component } from 'react';
import { SafeAreaView } from 'react-native';
import Carousel from 'react-native-snap-carousel';
import { sliderWidth, itemWidth } from './res/styles/SliderEntry.style';
import SliderEntry from './SliderEntry';
import styles from './res/styles/index.style';
import { ENTRIES1, ENTRIES2 } from './res/static/entries';

const SLIDER_1_FIRST_ITEM = 1;

export default class DrinkSelector extends Component {

    constructor (props) {
        super(props);
        this.state = {
            slider1ActiveSlide: SLIDER_1_FIRST_ITEM
        };
    }

    _renderItem ({item, index}) {
        return <SliderEntry data={item} even={(index + 1) % 2 === 0} />;
    }

    render () {
        return (
            <SafeAreaView style={styles.safeArea}>
                <Carousel
                  data={ENTRIES1}
                  renderItem={this._renderItem}
                  sliderWidth={sliderWidth}
                  itemWidth={itemWidth}
                  containerCustomStyle={styles.slider}
                  contentContainerCustomStyle={styles.sliderContentContainer}
                  layout={'tinder'}
                  loop={true}
                />
            </SafeAreaView>
        );
    }
}