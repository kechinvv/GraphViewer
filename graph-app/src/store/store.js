import { configureStore } from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'
import graph from '../features/graph/graphSlice'
import {graphApi}  from './api/graph.api'


export const store = configureStore({
  reducer: {
    graph,
    [graphApi.reducerPath]: graphApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(graphApi.middleware),
})

setupListeners(store.dispatch)