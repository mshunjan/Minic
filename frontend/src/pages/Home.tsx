import { Box, CircularProgress, Paper, Grid, Typography } from "@mui/material";
import { FormContainer } from "./StyledHome";
import { useMutation } from "react-query";
import { useUploads } from '../api/Uploads'
import { useState } from "react";
import CustomDropZone from "../components/CustomDropZone";
import testdataset from '../assets/testdataset.json'
import testbarchart from '../assets/testbarchart.json'

import ButtonAppBar from '../components/ButtonAppBar'
import Chart from '../components/Chart'
const Home = () => {
    const uploads = useUploads()
    const [data, setData] = useState(null)


    const send_upload = (files) => {
        return uploads.upload(files)
    }

    const upload = useMutation(send_upload, {
        onSuccess: (data: any) => {
            setData(data.data)
        },
        onError: (error: any) => {
            console.log(error)
        }
    })

    return (
        <Box display='flex' >
            <Grid
                container
                direction="row"
                justifyContent="center"
            >
                <Grid item xs={12}>
                    <ButtonAppBar />
                </Grid>
                <Grid item xs={12} p={2}>
                    <Grid container direction={'column'} justifyContent='center' alignContent={'center'}>
                            <FormContainer>
                                <Typography>Upload your file(s)!</Typography>
                                <Grid item xs={12} p={2}>
                                    {upload.isLoading ?

                                        <CircularProgress variant="indeterminate" />

                                        :
                                        data ?
                                            <>
                                                <Chart data={data} />
                                            </>
                                            :
                                            <CustomDropZone handleSubmit={upload.mutate} />
                                    }
                                </Grid>
                            </FormContainer>
                    </Grid>
                </Grid>
            </Grid>
        </Box>
    )
}

export default Home; 