import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { BrainScreen, SoulScreen, BodyScreen, ESQETScreen } from './src/screens';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Brain" component={BrainScreen} />
        <Tab.Screen name="Soul" component={SoulScreen} />
        <Tab.Screen name="Body" component={BodyScreen} />
        <Tab.Screen name="ESQET" component={ESQETScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
