/*
 * main.c
 * This file is part of PSR Registration Shuffler
 *
 * Copyright (C) 2008 - Dennis Schulmeister
 *
 * PSR Registration Shuffler is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * PSR Registration Shuffler is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with PSR Registration Shuffler; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor,
 * Boston, MA  02110-1301  USA
 *
 * PURPOSE:
 * ========
 *
 * This file compiles into a very simplistic bootstrap executable on 32-bit
 * Windows. Its purpose is to give Windows users an EXE file for starting
 * the application instead of a python script or the old batch file. The later
 * one had the disadvantage that it opened a mostly empty command line window
 * which would not vanish until the program ended.
 *
 * The compiled binary file needs to be copied to the root directoy of the
 * windows distribution - which is just a striped down python distribution
 * with the PSR Registration Shuffler included. There the executable tries to
 * invoke the local python interpreter.
 *
 * NOTE: The project file psrregshuffle.dev can be opened with the GPL'd
 * DevCPP 4.x from http://www.bloodshed.net.
 */

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
/*
int WINAPI WinMain (HINSTANCE hThisInstance,
                    HINSTANCE hPrevInstance,
                    LPSTR lpszArgument,
                    int nFunsterStil)
*/
int main(int argc, char *argv[]) {
    /* Local variables */
    int rc;
    STARTUPINFO startupInfo;
    PROCESS_INFORMATION processInfo;

    ZeroMemory(&startupInfo, sizeof(startupInfo));
    ZeroMemory(&processInfo, sizeof(processInfo));

    /* Make sure no python or command console appears */
    startupInfo.cb = sizeof(startupInfo);
    startupInfo.dwFlags = STARTF_USESHOWWINDOW;
    startupInfo.wShowWindow = SW_HIDE;

    /* Start application */
    rc = CreateProcess(
        NULL,                   /*Module name not explicitly given */
        "python.exe Scripts\\psrregshuffle",      /* Invoke local python interpreter */
        NULL,                           /* Don't inherit procces handle */
        NULL,                           /* Don't inherit thread handle */
        FALSE,                          /* Switch handle inheritance off */
        0,                              /* No special creation flags needed */
        NULL,                           /* Inherit environment block */
        NULL,                           /* Inherit procces directory */
        &startupInfo,                   /* Pointer to startup info structure */
        &processInfo                    /* Pointer to procces info structure */
    );

    if (!rc) {
        printf("Coudln't run the PSR Registration Shuffler: %d\n", GetLastError());
        return 1;
    }

    /* Close unnecessary handles and quit */
    CloseHandle(&processInfo.hProcess);
    CloseHandle(&processInfo.hThread);

    return 0;
}
