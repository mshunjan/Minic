import { Box, CircularProgress, Paper, Grid, Typography } from "@mui/material";
import { FormContainer, StyledButton } from "./StyledHome";
import { useMutation } from "react-query";
import { useUploads } from '../api/Uploads'
import { useEffect, useState } from "react";
import CustomDropZone from "../components/CustomDropZone";

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
                    <Paper>
                        <Typography variant='h1'>
                            MINIC
                        </Typography>
                    </Paper>
                </Grid>
                <Grid item xs={6} p={2}>
                    <FormContainer>
                        <Grid item xs={12} p={2}>
                            {upload.isLoading ?

                                <CircularProgress variant="indeterminate" />

                                :
                                upload.data ?
                                    JSON.stringify(data)
                                    :
                            <CustomDropZone handleSubmit={upload.mutate} />
                            }
                            </Grid>
                    </FormContainer>
                </Grid>
            </Grid>
        </Box>
    )
}

export default Home; 