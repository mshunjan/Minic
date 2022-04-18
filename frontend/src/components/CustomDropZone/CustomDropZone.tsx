import { useCallback, useEffect, useState } from 'react';
import { useDropzone } from 'react-dropzone'
import { Card, CardActionArea, Typography, Grid, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { StyledButton } from './StyledDropZone';
function CustomDropZone({ handleSubmit }) {
  const [files, setFiles] = useState([]);
  const [disabled, setDisabled] = useState(true);
  const [datafiles, setDataFiles] = useState([])

  const onDrop = useCallback(acceptedFiles => {
    setFiles([...files, ...acceptedFiles])
    setDisabled(false)
  }, [files])

  const { isDragActive, getRootProps, getInputProps, fileRejections } = useDropzone({
    onDrop,
    minSize: 0,
    multiple: true
  });

  useEffect(() => {
    if (files.length == 0) {
      setDisabled(true)
    } 
    // files.forEach(file => {
    //   const reader = new FileReader()
    //   reader.onload = () => {
    //     setDataFiles( prevState => [...prevState, reader.result])
    //   }
    //   reader.readAsDataURL(file)
    // })
  }, [files])


  const removeFile = file => () => {
    const newFiles = [...files]
    newFiles.splice(newFiles.indexOf(file), 1)
    setFiles(newFiles)
  } 

  const submitFN = () => {
    console.log(files)
    const formData = new FormData()
    files.forEach(file=> {
      formData.append('files', file)
    })
    handleSubmit(formData)

  }

  return (
    <>
      <Card variant="outlined">
        <CardActionArea>
          {/* {fileRejections.length > 0 ? <Alert severity='error'>Invalid File Type!</Alert> : null} */}
          <div {...getRootProps()}>
            <input {...getInputProps()} />
            {!isDragActive &&
              <Grid container justifyContent={'center'} alignItems={'center'}>
                <Grid item xs={12} p={2}>
                  <Typography variant='h6'>Click here or drop a file to upload!</Typography>

                </Grid>
              </Grid>}

          </div>
        </CardActionArea>
        <Card elevation={4}>
          {files.map(file => (
            <Grid container justifyContent={'center'} alignItems={'center'}>
              <Typography fontSize={11}>
                {file.path}
              </Typography>
              <IconButton onClick={removeFile(file)}><DeleteIcon /></IconButton>
            </Grid>
          ))}
        </Card>
      </Card>
      <StyledButton type="submit" variant={'contained'} disabled={disabled} onClick={() => submitFN()}>Submit</StyledButton>
    </>

  )
}
export default CustomDropZone;