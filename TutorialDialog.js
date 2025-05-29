import React, { useState } from "react";
import {
  Button,
  Dialog,
  DialogContent,
  Tabs,
  Tab,
  IconButton,
  Typography,
  Box,
  AppBar,
  Toolbar,
} from "@mui/material";
import { ArrowForward, ArrowBack, Close } from "@mui/icons-material";

// Sample data
const navigationOptions = [
  {
    id: 1,
    name: "Dashboard",
    tutorialSteps: [
      {
        id: 1,
        title: "Step 1: Overview",
        description:
          "This is the main dashboard where you can see all your metrics.",
        imageUrl: "https://via.placeholder.com/400x300?text=Dashboard+Step+1",
      },
      {
        id: 2,
        title: "Step 2: Metrics",
        description: "Here you can view your key performance indicators.",
        imageUrl: "https://via.placeholder.com/400x300?text=Dashboard+Step+2",
      },
    ],
  },
  {
    id: 2,
    name: "Profile",
    tutorialSteps: [
      {
        id: 1,
        title: "Step 1: Personal Info",
        description: "Update your personal information in this section.",
        imageUrl: "https://via.placeholder.com/400x300?text=Profile+Step+1",
      },
      {
        id: 2,
        title: "Step 2: Preferences",
        description: "Set your account preferences here.",
        imageUrl: "https://via.placeholder.com/400x300?text=Profile+Step+2",
      },
      {
        id: 3,
        title: "Step 3: Security",
        description: "Manage your security settings in this tab.",
        imageUrl: "https://via.placeholder.com/400x300?text=Profile+Step+3",
      },
    ],
  },
  {
    id: 3,
    name: "Settings",
    tutorialSteps: [
      {
        id: 1,
        title: "Step 1: General",
        description: "Configure general application settings.",
        imageUrl: "https://via.placeholder.com/400x300?text=Settings+Step+1",
      },
    ],
  },
];

const TutorialDialog = () => {
  const [open, setOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState(navigationOptions[0]);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  const handleOpen = () => {
    setOpen(true);
    setSelectedOption(navigationOptions[0]);
    setCurrentStepIndex(0);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleOptionSelect = (option) => {
    setSelectedOption(option);
    setCurrentStepIndex(0);
  };

  const handleNextStep = () => {
    if (
      selectedOption &&
      currentStepIndex < selectedOption.tutorialSteps.length - 1
    ) {
      setCurrentStepIndex(currentStepIndex + 1);
    }
  };

  const handlePrevStep = () => {
    if (currentStepIndex > 0) {
      setCurrentStepIndex(currentStepIndex - 1);
    }
  };

  return (
    <div>
      <Button variant="contained" color="primary" onClick={handleOpen}>
        Open Tutorial
      </Button>

      <Dialog
        open={open}
        onClose={handleClose}
        PaperProps={{
          style: {
            width: "800px",
            height: "600px",
            maxWidth: "none",
            maxHeight: "none",
          },
        }}
      >
        <AppBar position="static" color="default" elevation={0}>
          <Toolbar variant="dense" style={{ padding: 0 }}>
            <Tabs
              value={selectedOption.id}
              onChange={(e, newValue) => {
                const option = navigationOptions.find(
                  (opt) => opt.id === newValue
                );
                if (option) handleOptionSelect(option);
              }}
              indicatorColor="primary"
              textColor="primary"
              variant="fullWidth"
            >
              {navigationOptions.map((option) => (
                <Tab key={option.id} label={option.name} value={option.id} />
              ))}
            </Tabs>
            <IconButton
              onClick={handleClose}
              style={{ marginLeft: "auto", padding: "8px" }}
              size="large"
            >
              <Close fontSize="large" />
            </IconButton>
          </Toolbar>
        </AppBar>

        <DialogContent
          style={{
            display: "flex",
            flexDirection: "column",
            height: "100%",
            padding: 0,
            position: "relative",
          }}
        >
          <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            justifyContent="center"
            height="100%"
            position="relative"
          >
            {/* Left click area for previous step */}
            <Box
              position="absolute"
              left={0}
              top={0}
              bottom={0}
              width="30%"
              display="flex"
              alignItems="center"
              justifyContent="flex-start"
              onClick={handlePrevStep}
              style={{ cursor: currentStepIndex > 0 ? "pointer" : "default" }}
            >
              {currentStepIndex > 0 && (
                <IconButton
                  color="primary"
                  style={{ fontSize: "3rem" }}
                  size="large"
                >
                  <ArrowBack fontSize="inherit" />
                </IconButton>
              )}
            </Box>

            {/* Content area */}
            <Box textAlign="center" width="40%" px={2}>
              <Typography variant="h5" gutterBottom>
                {selectedOption.tutorialSteps[currentStepIndex].title}
              </Typography>
              <Typography paragraph>
                {selectedOption.tutorialSteps[currentStepIndex].description}
              </Typography>
              <Box my={2}>
                <img
                  src={selectedOption.tutorialSteps[currentStepIndex].imageUrl}
                  alt={selectedOption.tutorialSteps[currentStepIndex].title}
                  style={{
                    maxWidth: "100%",
                    maxHeight: "300px",
                    border: "1px solid #ddd",
                    borderRadius: "4px",
                  }}
                />
              </Box>
              <Typography>
                Step {currentStepIndex + 1} of{" "}
                {selectedOption.tutorialSteps.length}
              </Typography>
            </Box>

            {/* Right click area for next step */}
            <Box
              position="absolute"
              right={0}
              top={0}
              bottom={0}
              width="30%"
              display="flex"
              alignItems="center"
              justifyContent="flex-end"
              onClick={handleNextStep}
              style={{
                cursor:
                  currentStepIndex < selectedOption.tutorialSteps.length - 1
                    ? "pointer"
                    : "default",
              }}
            >
              {currentStepIndex < selectedOption.tutorialSteps.length - 1 && (
                <IconButton
                  color="primary"
                  style={{ fontSize: "3rem" }}
                  size="large"
                >
                  <ArrowForward fontSize="inherit" />
                </IconButton>
              )}
            </Box>
          </Box>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default TutorialDialog;
