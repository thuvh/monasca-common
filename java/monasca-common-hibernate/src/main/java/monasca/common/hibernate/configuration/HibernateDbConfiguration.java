/*
 * Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package monasca.common.hibernate.configuration;

import com.fasterxml.jackson.annotation.JsonProperty;

public class HibernateDbConfiguration {

  @JsonProperty
  boolean supportEnabled;
  @JsonProperty
  String providerClass;
  @JsonProperty
  String dataSourceClassName;
  @JsonProperty
  String serverName;
  @JsonProperty
  String portNumber;
  @JsonProperty
  String databaseName;
  @JsonProperty
  String user;
  @JsonProperty
  String password;
  @JsonProperty
  String initialConnections;
  @JsonProperty
  String maxConnections;
  @JsonProperty
  String autoConfig;

  public boolean getSupportEnabled() {
    return supportEnabled;
  }

  public String getProviderClass() {
    return providerClass;
  }

  public void setProviderClass(String providerClass) {
    this.providerClass = providerClass;
  }

  public String getDataSourceClassName() {
    return dataSourceClassName;
  }

  public String getServerName() {
    return serverName;
  }

  public String getPortNumber() {
    return portNumber;
  }

  public String getDatabaseName() {
    return databaseName;
  }

  public String getUser() {
    return user;
  }

  public String getPassword() {
    return password;
  }

  public String getInitialConnections() {
    return initialConnections;
  }

  public String getMaxConnections() {
    return maxConnections;
  }

  public String getAutoConfig() {
    return autoConfig;
  }
}
