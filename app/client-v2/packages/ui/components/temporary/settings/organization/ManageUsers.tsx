import { useState } from "react";
import React from "react";

import { makeStyles } from "../../../../lib/ThemeProvider";
import { EnhancedTable } from "../../../DataDisplay";
import Dialog from "../../../Dialog";
import { SelectField, TextField, Switch } from "../../../Inputs";
import Modal from "../../../Modal";
import { Card } from "../../../Surfaces";
import Banner from "../../../Surfaces/Banner";
import { Icon, Button, Text } from "../../../theme";

interface RowsType extends Object {
  name: string;
  email: string;
  role: string;
  status: React.ReactNode;
  Added: string;
}

const ManageUsers = () => {
  const { classes } = useStyles();

  // Component States
  const [userInDialog, setUserInDialog] = useState<RowsType | null>();
  const [addUserDialog, setAddUserDialog] = useState(false);
  const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(null);
  const [ismodalVisible, setModalVisible] = useState<boolean>(false);
  const [extensions, setExtensions] = useState<
    {
      id: string;
      extension: string;
      studyarea: string;
      maxPlaces: number;
      checked: boolean;
      placesLeft: number;
    }[]
  >([
    {
      id: "1",
      extension: "Active mobility",
      studyarea: "Greater Munich",
      maxPlaces: 3,
      placesLeft: 1,
      // available: "1 of 3 seats available",
      checked: false,
    },
    {
      id: "2",
      extension: "Motorised mobility",
      studyarea: "Greater Munich",
      maxPlaces: 3,
      placesLeft: 0,
      checked: false,
    },
    {
      id: "3",
      extension: "Active mobility",
      studyarea: "Berlin",
      maxPlaces: 3,
      placesLeft: 2,
      checked: false,
    },
    {
      id: "4",
      extension: "Active mobility",
      studyarea: "London",
      maxPlaces: 3,
      placesLeft: 3,
      checked: false,
    },
  ]);

  const columnNames = [
    {
      id: "name",
      numeric: false,
      label: "Name",
    },
    {
      id: "email",
      numeric: false,
      label: "E-mail",
    },
    {
      id: "role",
      numeric: false,
      label: "Role",
    },
    {
      id: "status",
      numeric: false,
      label: "Status",
    },
    {
      id: "added",
      numeric: false,
      label: "Added",
    },
  ];

  const rows: RowsType[] = [
    {
      name: "Luca William Silva",
      email: "john.wloremipsum@gmail.com",
      role: "Admin",
      status: (
        <Button startIcon="check" className={classes.buttonSmall}>
          Active
        </Button>
      ),
      Added: "23 Jun 19",
    },
    {
      name: "Fenix William Silva",
      email: "john.wloremipsum@gmail.com",
      role: "Admin",
      status: (
        <Button variant="secondary" startIcon="email" className={classes.buttonSmall}>
          Invite sent
        </Button>
      ),
      Added: "23 Jun 19",
    },
    {
      name: "Adam William Silva",
      email: "john.wloremipsum@gmail.com",
      role: "Admin",
      status: (
        <Button variant="warning" startIcon="warnOutlined" className={classes.buttonSmall}>
          Expired
        </Button>
      ),
      Added: "23 Jun 19",
    },
    {
      name: "John William Silva",
      email: "john.wloremipsum@gmail.com",
      role: "Admin",
      status: (
        <Button startIcon="check" className={classes.buttonSmall}>
          Active
        </Button>
      ),
      Added: "23 Jun 19",
    },
    {
      name: "John William Silva",
      email: "john.wloremipsum@gmail.com",
      role: "Admin",
      status: (
        <Button variant="secondary" startIcon="email" className={classes.buttonSmall}>
          Invite sent
        </Button>
      ),
      Added: "23 Jun 19",
    },
    {
      name: "John William Silva",
      email: "john.wloremipsum@gmail.com",
      role: "Admin",
      status: (
        <Button variant="secondary" startIcon="email" className={classes.buttonSmall}>
          Invite sent
        </Button>
      ),
      Added: "23 Jun 19",
    },
  ];

  // Functions

  /**
   * Updates the state of the extensions array based on the provided element name and checked value
   * @param {React.ChangeEvent<HTMLInputElement>} event - The change event object.
   * @param {boolean} checked - The new checked state of the switch.
   * @param {string | undefined} elementName - The name of the element associated with the switch.
   */

  function handleSwitch(
    event: React.ChangeEvent<HTMLInputElement>,
    checked: boolean,
    elementName: string | undefined
  ) {
    if (elementName) {
      extensions.forEach((ext, index) => {
        if (ext.id === elementName) {
          const newExtensionState = extensions;
          if (checked) {
            newExtensionState[index].placesLeft--;
          } else {
            newExtensionState[index].placesLeft++;
          }
          newExtensionState[index].checked = !ext.checked;
          setExtensions([...newExtensionState]);
        }
      });
    }
  }

  function openAddUserDialog(event: React.MouseEvent<HTMLButtonElement>) {
    setAnchorEl(event.currentTarget);
    setAddUserDialog(true);
  }

  function handleAddUserClose() {
    setAnchorEl(null);
    setAddUserDialog(false);
  }

  function openModal() {
    setModalVisible(true);
  }

  return (
    <div>
      <div className={classes.container}>
        <div className={classes.head}>
          <Icon
            iconId="user"
            wrapped="circle"
            bgVariant="gray2"
            bgOpacity={0.6}
            iconVariant="secondary"
            size="medium"
          />
          <Text typo="body 1" className={classes.name}>
            Organization name
          </Text>
        </div>
        <div className={classes.search}>
          <TextField className={classes.searchInput} type="text" label="Search" size="small" />
          <Icon iconId="filter" size="medium" iconVariant="gray" />
          <div style={{ position: "relative" }}>
            <Button onClick={openAddUserDialog} className={classes.searchButton}>
              Invite user
            </Button>
            {/* Invite User Dialog */}
            {addUserDialog ? (
              <Dialog
                title="Invite team mate"
                width="444px"
                direction="right"
                anchorEl={anchorEl}
                action={
                  <div className={classes.buttons}>
                    <Button variant="noBorder" onClick={handleAddUserClose}>
                      CANCEL
                    </Button>
                    <Button variant="noBorder">SEND INVITATION</Button>
                  </div>
                }
                onClick={handleAddUserClose}>
                <div className={classes.head}>
                  <Icon
                    iconId="user"
                    wrapped="circle"
                    bgVariant="gray2"
                    bgOpacity={0.6}
                    iconVariant="secondary"
                    size="small"
                  />
                  <Text typo="body 1">Organization name</Text>
                </div>
                <Text typo="body 3">
                  Send an invitation via email <br /> The receiver will get a link with 72 hours of expiration
                </Text>
                <div className={classes.formInputs}>
                  <TextField size="small" type="email" label="Email address" />
                  <SelectField
                    size="small"
                    defaultValue="editor"
                    label="Permission"
                    options={[
                      {
                        name: "Editor",
                        value: "editor",
                      },
                      {
                        name: "Admin",
                        value: "admin",
                      },
                      {
                        name: "Guest",
                        value: "guest",
                      },
                    ]}
                  />
                </div>
              </Dialog>
            ) : null}
          </div>
        </div>
      </div>
      <Card noHover={true} className={classes.tableCard}>
        {/* ManageUsers Table */}
        <EnhancedTable
          rows={rows}
          columnNames={columnNames}
          openDialog={setUserInDialog}
          // User Info Dialog
          dialog={{
            title: userInDialog ? userInDialog.name : "unknown",
            action: (
              <div style={{ textAlign: "right" }}>
                <Button onClick={openModal} variant="noBorder">
                  REMOVE USER
                </Button>
              </div>
            ),
            body: (
              <div>
                <div className={classes.userDataContainer}>
                  <span className={classes.userDataText}>
                    <Text typo="body 2" className={classes.userDataTitle}>
                      Name:{" "}
                    </Text>{" "}
                    <Text typo="label 2">{userInDialog ? userInDialog?.name : ""}</Text>
                  </span>
                  <span className={classes.userDataText}>
                    <Text typo="body 2" className={classes.userDataTitle}>
                      E-mail:{" "}
                    </Text>{" "}
                    <Text typo="label 2">{userInDialog ? userInDialog?.email : ""}</Text>
                  </span>
                  <span className={classes.userDataText}>
                    <Text typo="body 2" className={classes.userDataTitle}>
                      Added in:{" "}
                    </Text>{" "}
                    <Text typo="label 2">{userInDialog ? userInDialog?.Added : ""}</Text>
                  </span>
                  <span className={classes.userDataText}>
                    <Text typo="body 2" className={classes.userDataTitle}>
                      Last Active:{" "}
                    </Text>{" "}
                    <Text typo="label 2">3 days ago</Text>
                  </span>
                  <span className={classes.userDataText}>
                    <Text typo="body 2" className={classes.userDataTitle}>
                      Organisation role:{" "}
                    </Text>{" "}
                    <Text typo="label 2">{userInDialog ? userInDialog?.role : ""}</Text>
                  </span>
                  <span className={classes.userDataText}>
                    <Text typo="body 2" className={classes.userDataTitle}>
                      Status:{" "}
                    </Text>{" "}
                    <Text typo="label 2">{userInDialog ? userInDialog?.status : ""}</Text>
                  </span>
                </div>
                {extensions.map((extension, indx) => (
                  <div key={indx} className={classes.switcher}>
                    <Switch
                      checked={extension.checked}
                      onChecked={handleSwitch}
                      elementName={extension.id}
                      disabled={!extension.placesLeft && !extension.checked}
                    />
                    <Text typo="body 1">
                      {extension.extension} - {extension.studyarea}
                    </Text>
                    <Text typo="caption" color="secondary">
                      {extension.placesLeft} of {extension.maxPlaces} seats available
                    </Text>
                  </div>
                ))}
              </div>
            ),
          }}
        />
      </Card>
      <Banner
        actions={<Button>Subscribe Now</Button>}
        content={
          <Text className={classes.bannerText} typo="body 1">
            Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean
            massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.{" "}
          </Text>
        }
        image="https://s3-alpha-sig.figma.com/img/630a/ef8f/d732bcd1f3ef5d6fe31bc6f94ddfbca8?Expires=1687132800&Signature=aJvQ22UUlmvNjDlrgzV6MjJK~YgohUyT9mh8onGD-HhU5yMI0~ThWZUGVn562ihhRYqlyiR5Rskno84OseNhAN21WqKNOZnAS0TyT3SSUP4t4AZJOmeuwsl2EcgElMzcE0~Qx2X~LWxor1emexxTlWntivbnUeS6qv1DIPwCferjYIwWsiNqTm7whk78HUD1-26spqW3AXVbTtwqz3B8q791QigocHaK9b4f-Ulrk3lsmp8BryHprwgetHlToFNlYYR-SqPFrEeOKNQuEDKH0QzgGv3TX7EfBNL0kgP3Crued~JNth-lIEPCjlDRnFQyNpSiLQtf9r2tH9xIsKA~XQ__&Key-Pair-Id=APKAQ4GOSFWCVNEHN3O4"
        imageSide="right"
      />
      {/* Confirm User Removal */}
      <Modal
        width="444px"
        open={ismodalVisible}
        changeOpen={setModalVisible}
        action={
          <>
            <Button onClick={() => setModalVisible(false)} variant="noBorder">
              CANCEL
            </Button>
            <Button onClick={() => setModalVisible(false)} variant="noBorder">
              CONFIRM
            </Button>
          </>
        }
        header={
          <Text className={classes.modalHeader} typo="object heading">
            <Icon iconId="warn" iconVariant="warning" /> Attention
          </Text>
        }>
        <Text typo="body 1">
          By removing a user they won&apos;t be able to access any projects under your organisation
        </Text>
      </Modal>
    </div>
  );
};

const useStyles = makeStyles({ name: { ManageUsers } })((theme) => ({
  bannerText: {
    color: "white",
    "@media (max-width: 1268px)": {
      fontSize: "14px",
    },
  },
  name: {
    fontWeight: "bold",
  },
  head: {
    display: "flex",
    alignItems: "center",
    gap: theme.spacing(2),
    marginBottom: theme.spacing(3),
  },
  buttons: {
    display: "flex",
    alignItems: "center",
    justifyContent: "end",
    gap: theme.spacing(2),
  },
  search: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: theme.spacing(4),
    marginBottom: theme.spacing(3),
  },
  searchButton: {
    width: "131px",
  },
  container: {
    padding: `0px ${theme.spacing(3)}px`,
    marginBottom: theme.spacing(2),
  },
  searchInput: {
    flexGrow: "1",
  },
  tableCard: {
    padding: theme.spacing(3),
    marginBottom: theme.spacing(5),
  },
  userDataContainer: {
    border: `1px solid ${theme.colors.palette[theme.isDarkModeEnabled ? "dark" : "light"].greyVariant1}`,
    padding: theme.spacing(3),
    borderRadius: 4,
  },
  userDataText: {
    display: "flex",
    gap: theme.spacing(1),
    alignItems: "center",
    marginBottom: theme.spacing(2),
  },
  userDataTitle: {
    fontWeight: "800",
  },
  formInputs: {
    marginTop: theme.spacing(3),
    display: "flex",
    flexDirection: "column",
    gap: theme.spacing(2),
  },
  modalHeader: {
    display: "flex",
    alignItems: "center",
    gap: theme.spacing(1),
  },
  buttonSmall: {
    padding: "3px 10px",
  },
  switcher: {
    display: "flex",
    alignItems: "center",
    gap: theme.spacing(1),
  },
}));

export default ManageUsers;
