import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  nodes: [],
  edges: [],
}
// incoming json
// {nodes: [], edges:[] }

export const graphSlice = createSlice({
  name: 'graph',
  initialState,
  reducers: {
    setNodes: (state, nodes) => {
        state.nodes = nodes.payload
    },
    setEdges: (state, edges) => {
        state.edges = edges.payload
    },
  },
})

export const { setNodes, setEdges } = graphSlice.actions

export default graphSlice.reducer