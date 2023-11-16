import { createSlice } from '@reduxjs/toolkit'

const initialState = {
    model: "ast"
}

export const modelSlice = createSlice({
  name: 'model',
  initialState,
  reducers: {
    setModel: (state, newModel) => {
        state.model = newModel
    },
  },
})

export const { setModel } = modelSlice.actions

export default modelSlice.reducer