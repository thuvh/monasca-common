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
package monasca.common.hibernate.db;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.Id;
import javax.persistence.Table;
import monasca.common.hibernate.db.CreateUpdateDate;
import monasca.common.model.alarm.AlarmNotificationMethodType;
import org.joda.time.DateTime;

@Entity
@Table(name = "notification_method")
public class NotificationMethodDb extends CreateUpdateDate{

  @Id
  @Column(name = "id", length = 36)
  private String id;

  @Column(name = "tenant_id", length = 36)
  private String tenant_id;

  @Column(name = "name", length = 250)
  private String name;

  @Column(name = "type")
  @Enumerated(EnumType.STRING)
  private AlarmNotificationMethodType type;

  @Column(name = "address", length = 100)
  private String address;

  public NotificationMethodDb() {
    super();
  }

  public NotificationMethodDb(String id, String tenant_id, String name, AlarmNotificationMethodType type, String address, DateTime created_at,
      DateTime updated_at) {
    super(created_at, updated_at);
    this.id = id;
    this.tenant_id = tenant_id;
    this.name = name;
    this.type = type;
    this.address = address;
  }

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public String getTenant_id() {
    return tenant_id;
  }

  public void setTenant_id(String tenant_id) {
    this.tenant_id = tenant_id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public AlarmNotificationMethodType getType() {
    return type;
  }

  public void setType(AlarmNotificationMethodType type) {
    this.type = type;
  }

  public String getAddress() {
    return address;
  }

  public void setAddress(String address) {
    this.address = address;
  }
}
