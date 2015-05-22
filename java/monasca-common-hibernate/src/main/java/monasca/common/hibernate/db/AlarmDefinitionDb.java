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

import monasca.common.model.alarm.AlarmSeverity;

import org.hibernate.annotations.Parameter;
import org.hibernate.annotations.Type;
import org.joda.time.DateTime;

@Entity
@Table(name = "alarm_definition")
public class AlarmDefinitionDb extends CreateUpdateDate{

  @Id
  @Column(name = "id", length = 36)
  private String id;

  @Column(name = "tenant_id", length = 36)
  private String tenant_id;

  @Column(name = "name", length = 250)
  private String name;

  @Column(name = "description", length = 250)
  private String description;

  @Column(name = "expression", columnDefinition = "TEXT")
  private String expression;

  @Column(name = "severity")
  @Enumerated(EnumType.STRING)
  private AlarmSeverity severity;

  @Column(name = "match_by", length = 255)
  private String match_by;

  @Column(name = "actions_enabled", length = 1, nullable = false)
  private int actions_enabled = 1;

  @Column(name = "deleted_at")
  @Type(type = "org.jadira.usertype.dateandtime.joda.PersistentDateTime", parameters = {@Parameter(name = "databaseZone", value = "UTC"),
      @Parameter(name = "javaZone", value = "jvm")})
  private DateTime deleted_at;

  public AlarmDefinitionDb() {
    super();
  }

  public AlarmDefinitionDb(String id, String tenant_id, String name, String description, String expression, AlarmSeverity severity, String match_by,
      int actions_enabled, DateTime created_at, DateTime updated_at, DateTime deleted_at) {
    super(created_at, updated_at);
    this.id = id;
    this.tenant_id = tenant_id;
    this.name = name;
    this.description = description;
    this.expression = expression;
    this.severity = severity;
    this.match_by = match_by;
    this.actions_enabled = actions_enabled;
    this.deleted_at = deleted_at;
  }

  public AlarmDefinitionDb(String id, String tenant_id, String expression, AlarmSeverity severity, DateTime created_at, DateTime updated_at) {
    super(created_at, updated_at);
    this.id = id;
    this.tenant_id = tenant_id;
    this.expression = expression;
    this.severity = severity;
    this.match_by = "";
    this.actions_enabled = 1;
    this.name = null;
    this.description = null;
    this.deleted_at = null;
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

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public String getExpression() {
    return expression;
  }

  public void setExpression(String expression) {
    this.expression = expression;
  }

  public AlarmSeverity getSeverity() {
    return severity;
  }

  public void setSeverity(AlarmSeverity severity) {
    this.severity = severity;
  }

  public String getMatch_by() {
    return match_by;
  }

  public void setMatch_by(String match_by) {
    this.match_by = match_by;
  }

  public int isActions_enabled() {
    return actions_enabled;
  }

  public void setActions_enabled(int actions_enabled) {
    this.actions_enabled = actions_enabled;
  }

  public DateTime getDeleted_at() {
    return deleted_at;
  }

  public void setDeleted_at(DateTime deleted_at) {
    this.deleted_at = deleted_at;
  }

  @Override
  public String toString() {
    return id;
  }
}
